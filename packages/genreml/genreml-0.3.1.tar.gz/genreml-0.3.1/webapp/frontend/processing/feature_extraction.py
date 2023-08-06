from genreml.model.processing import audio


def process_audio_file(location: str) -> tuple:
    """ Given a location of an uploaded file, this will run feature extraction and return a tuple containing lists
    of features + images to be displayed to the user

    :param location - the location of a file to extract audio features from
    :returns tuple containing the lists of features extracted
    """
    audio_files = audio.AudioFiles()
    audio_files.extract_features(location, cmap=None)
    return audio_files.features, audio_files.visual_features
