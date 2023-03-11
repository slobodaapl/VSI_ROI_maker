import pickle


def reset_dict(skip_dict_path: str):
    # load pickled dict
    with open(skip_dict_path, 'rb') as f:
        skip_dict = pickle.load(f)

    # reset all 'done' values to False
    for file in skip_dict:
        skip_dict[file]['done'] = False
        skip_dict[file]['idx'] = 0
        skip_dict[file]['file_idx'] = 0

    # save the reset dict
    with open(skip_dict_path, 'wb') as f:
        pickle.dump(skip_dict, f)


if __name__ == "__main__":
    reset_dict('skip_dict.pkl')
