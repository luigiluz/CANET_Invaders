import subprocess
import multiprocessing
import time

ATTACKS_PARAMETER_DICT = {
    "doS": {
        "id": "000",
        "dlc": 8,
        "binary": 0,
        "period": 0.004
    },
    # "falsifying": {
    #     "id": "00E",
    #     "dlc": 8,
    #     "binary": 0,
    #     "period": 0.00875    # "falsifying": {
    #     "id": "00E",
    #     "dlc": 8,
    #     "binary": 0,
    #     "period": 0.00875
    # },
    # "fuzzing": {
    #     "id": "000",
    #     "dlc": 8,
    #     "binary": 0,
    #     "period": 0.95
    # },
    # "impersonation": {
    #     "id": "05C",
    #     "dlc": 4,
    #     "binary": 0,
    #     "period": 0.05
    # }
    # },
    # "fuzzing": {
    #     "id": "000",
    #     "dlc": 8,
    #     "binary": 0,
    #     "period": 0.95
    # },
    # "impersonation": {
    #     "id": "05C",
    #     "dlc": 4,
    #     "binary": 0,
    #     "period": 0.05
    # }
}

CAN_INTERFACE = "vcan0"
PERIOD_OF_TIME = 10

def run_candump():
    dump_time = 3*PERIOD_OF_TIME

    process = subprocess.Popen(["candump", CAN_INTERFACE, "-t", "z", "-l", "-x"])
    time.sleep(dump_time)
    process.terminate()

    print(f"Candump concluded after {dump_time} seconds")


def run_malicious_attack(attack, can_id, dlc, binary, period):
    time.sleep(PERIOD_OF_TIME)
    process = subprocess.Popen(["python3", "/home/luigi/workspace/CAN_Invaders/src/CAN_Invaders/scripts/malicious_attack.py", "-c", CAN_INTERFACE, "--type", f"{attack}", "--sleep", f"{period}", "-m", f"{can_id}", f"{dlc}", f"{binary}"])
    time.sleep(PERIOD_OF_TIME)
    process.terminate()

    print(f"Malicious attack was concluded after waiting for {PERIOD_OF_TIME} seconds and executed for {PERIOD_OF_TIME} seconds")

def main():
    print("Executing attacks")

    for attack, parameters in ATTACKS_PARAMETER_DICT.items():
        print(f"Current attack: {attack}")

        can_id = parameters['id']
        dlc = parameters['dlc']
        binary = parameters['binary']
        period = parameters['period']

        candump_process = multiprocessing.Process(target=run_candump)
        malicious_attack_process = multiprocessing.Process(target=run_malicious_attack, args=(attack, can_id, dlc, binary, period, ))

        candump_process.start()
        malicious_attack_process.start()

        candump_process.join()
        malicious_attack_process.join()

if __name__ == "__main__":
    main()
