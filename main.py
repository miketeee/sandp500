from src.flows import transformationflows, extractionflows
from prefect import flow
from prefect.filesystems import S3

s3_block = S3.load("sandp-s3-block")

@flow(name="main flow")
def main_flow():
    extractionflows.get_s_and_p_500_companies()
    transformationflows.data_cleaning()


if __name__ == '__main__':
    main_flow()








