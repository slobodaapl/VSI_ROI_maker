import os
import pickle
from cv2 import imwrite
import time

from vsiprocessor.vsi_file import VSIFile
from vsiprocessor.vsi_entropy import vsi_has_sufficient_information


def load_dict(path: str):
    # load pickled dict
    with open(path, 'rb') as f:
        return pickle.load(f)


def main(skip_dict_path: str, data_dir: str = 'data', save_dir: str = 'processed', retries=10, wait_retry=30):
    # check if dictionary exists as a file
    if os.path.isfile(skip_dict_path):
        # load the dictionary
        skip_dict = load_dict(skip_dict_path)
    else:
        # create a new dictionary
        skip_dict = {}

    # check if save_dir folder exists, and if not, make it
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    # check if save_dir folder contains 'he' and 'p63' folders, and if not, make them
    if not os.path.isdir(os.path.join(save_dir, 'he')):
        os.mkdir(os.path.join(save_dir, 'he'))

    if not os.path.isdir(os.path.join(save_dir, 'p63')):
        os.mkdir(os.path.join(save_dir, 'p63'))

    # save 'he' and 'p63' folders to variables
    he_dir = os.path.join(save_dir, 'he')
    p63_dir = os.path.join(save_dir, 'p63')

    for file in os.listdir(data_dir):
        if not file.endswith('.vsi'):
            continue

        # check if the .vsi file is 'he' or 'p63'
        if 'he' in file:
            img_type = 'he'
        elif 'p63' in file:
            img_type = 'p63'
        else:
            raise ValueError(f'File {file} is not of type "he" or "p63"')

        if file not in skip_dict:
            skip_dict[file] = {'done': False, 'idx': 0, 'file_idx': 0, 'skip': []}
        elif skip_dict[file]['done']:
            continue

        with VSIFile(os.path.abspath(os.path.join(data_dir, file)), skip_dict=skip_dict[file]) as vsi:
            file_idx = skip_dict[file]['file_idx']
            for roi in vsi:
                if vsi_has_sufficient_information(roi):
                    for i in range(retries):
                        try:
                            if img_type == 'he':
                                imwrite(os.path.join(he_dir, f'{file_idx}.png'), roi)
                            else:
                                imwrite(os.path.join(p63_dir, f'{file_idx}.png'), roi)
                        except Exception as e:
                            if i < retries - 1:
                                print(f'Error saving image {file_idx}: {e}')
                                time.sleep(wait_retry)
                                continue
                            else:
                                raise
                        break

                    file_idx += 1
                    skip_dict[file]['file_idx'] = file_idx

                else:
                    skip_dict[file]['skip'].append(vsi.idx - 1)

                # save dictionary every 50 procesed images regardless of whether they were skipped or not
                if vsi.idx % 50 == 0:
                    with open(skip_dict_path, 'wb') as f:
                        pickle.dump(skip_dict, f)

            skip_dict[file]['done'] = True

            # save dictionary after each file
            with open(skip_dict_path, 'wb') as f:
                pickle.dump(skip_dict, f)

        print(f'Finished processing {file}')


if __name__ == '__main__':
    main('skip_dict.pkl')
