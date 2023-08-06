from locative_ml_helpers.platform_helpers.gcp.environment import Environment
import argparse

def str2bool(arg_value: str) -> bool:
    if isinstance(arg_value, bool):
        return arg_value
    if arg_value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif arg_value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':

    PARSER= argparse.ArgumentParser()
    ## User set params which link to Sagemaker params
    PARSER.add_argument('--prod', type=str2bool,
                        default=False,
                        help='Expects a .csv file, representing the lookup.')
    ARGS, _ = PARSER.parse_known_args()
    print("Setting up Environment")
    env = Environment(base_dir='/opt/ml/')
    if ARGS.prod:
        env.setup_input_data()
    print("Done")
