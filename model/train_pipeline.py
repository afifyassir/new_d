import sys
from pathlib import Path

from sklearn.model_selection import train_test_split

# Add the root of your project to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from model.config.core import config  # noqa: E402
from model.pipeline import pipe  # noqa: E402
from model.preprocessing.data_manager import load_dataset, save_pipeline  # noqa: E402


def run_training() -> None:
    """
    Train the model.

    Training data can be found here:
    https://www.openml.org/data/get_csv/16826755/phpMYEkMl
    """

    # read training data
    data = load_dataset(
        client_file_name=config.app_config.client_data_file,
        price_file_name=config.app_config.price_data_file,
    )

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )

    # fit model
    pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=pipe)


if __name__ == "__main__":
    run_training()
