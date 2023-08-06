import os


class UfwConfigGenerator:
    def generate(_, port: int, accept: bool = False):
        if accept == True:
            os.system(f"ufw allow {port}")
        else:
            os.system(f"ufw deny {port}")

    def reload():
        raise NotImplementedError()
