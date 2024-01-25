import json
from pathlib import Path

from icecream import ic

guests_dict_fn = lambda item: item["guests"]


def main():
    history_file = Path("outputs/history/items.jsonl")
    items = [json.loads(line) for line in history_file.open("r").readlines()]
    # Extend with recent appearences
    current_file = Path("outputs/current/cca2c193-83eb-46c2-9c81-3a47aaa616cc.jsonl")
    for line in current_file.open("r").readlines():
        items.append(json.loads(line))
    num_episodes = len(items)
    num_guests_per_episode = []
    guest_names = []
    for guest_list in list(map(guests_dict_fn, items)):
        for guest in guest_list:
            guest_names.append(guest["name"])
        num_guests_per_episode.append(len(guest_list))
    unqiue_guests = set(guest_names)

    average_guests_per_episode = sum(num_guests_per_episode) / num_episodes
    print(f"Number of episodes: {num_episodes}")
    print(f"Unique guest: {len(unqiue_guests)}")
    print(f"Average guests per episode {average_guests_per_episode}")

    guest2freq = {name: 0 for name in unqiue_guests}
    for name in guest_names:
        guest2freq[name] += 1
    guest2freq_sorted = {
        k: v for k, v in sorted(guest2freq.items(), key=lambda item: item[1], reverse=True)
    }
    print("Appearences per guest:")
    for guest, freq in guest2freq_sorted.items():
        print(guest, freq)

    all_roles = []
    for guest_list in list(map(guests_dict_fn, items)):
        for guest in guest_list:
            print(guest["role"])
            all_roles.append(guest["role"])

    unqiue_roles = list(set(all_roles))
    # ic(unqiue_roles)

    expert_role_fn = lambda role: "expertin" in role.lower() or "experte" in role.lower()
    expert_roles = list(filter(expert_role_fn, unqiue_roles))
    ic(expert_roles)

    experts = {}
    for guest_list in list(map(guests_dict_fn, items)):
        for guest in guest_list:
            if guest["role"] in expert_roles:
                if not guest["name"] in experts.keys():
                    experts[guest["name"]] = [guest["role"]]
                else:
                    experts[guest["name"]].append(guest["role"])
                    experts[guest["name"]] = list(set(experts[guest["name"]]))
    ic(experts)

    # guest_roles = {}
    # for guest_list in list(map(guests_dict_fn, items)):
    #     for guest in guest_list:
    #         if not guest["name"] in guest_roles.keys():
    #             guest_roles[guest["name"]] = [guest["role"]]
    #         else:
    #             guest_roles[guest["name"]].append(guest["role"])
    #
    # for guest_name in guest_roles.keys():
    #     guest_roles[guest_name] = list(set(guest_roles[guest_name]))
    #     print(guest_name, guest_roles[guest_name])


if __name__ == "__main__":
    main()
