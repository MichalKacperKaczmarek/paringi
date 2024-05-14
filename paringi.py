import pprint
import csv
from pathlib import Path
from typing import Optional

NAME = 'Name'
TP = 'TP'
VP = 'VP'
OP = 'OP'

FIELD_NAMES = [NAME, TP, OP, VP]

Wysuszony = 'Wysuszony'
Pobozny = 'Pobozny'
Kampftanzer = 'Kampftanzer'
Grzyboluby = 'Grzyboluby'
Spustoszyciel = 'Spustoszyciel'
Zapujczyciel = 'Zapujczyciel'
Swiniojebca = 'Swiniojebca'
Paladyn_Malorosly = 'Paladyn Malorosly'

PLAYERS = (
    Wysuszony,
    Pobozny,
    Kampftanzer,
    Grzyboluby,
    Spustoszyciel,
    Zapujczyciel,
    Swiniojebca,
    Paladyn_Malorosly
)

folder_path = Path(r'C:\smici')
file_name = 'pierwsza_wroclawska_liga_kekekek.csv'
pairing_file = 'paringi.csv'


def initialize_player_table(players: tuple, path_to_folder: Path, filename: str) -> None:
    with open(Path(path_to_folder, filename), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for player in players:
            writer.writerow({NAME: player, TP: 0, VP: 0, OP: 0})


def read_players_table(path_to_folder: Path, filename: str) -> list:
    with open(Path(path_to_folder, filename), 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def add_pairing(path_to_folder: Path, filename: str, player_1: str, player_2: str) -> None:
    with open(Path(path_to_folder, filename), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow({player_1, player_2})


def read_pairings(path_to_folder: Path, filename: str) -> list:
    with open(Path(path_to_folder, filename), 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        return[set(row) for row in reader]


def sort_players_and_remove_bye(path_to_folder: Path, filename: str, player_bye: Optional[str]):
    players_list = read_players_table(path_to_folder, filename)
    sorted_player_list = sorted(players_list, reverse=True, key=lambda k: (int(k['TP']), int(k['OP']), int(k['VP'])))
    if player_bye:
        sorted_player_list = remove_player_from_list(sorted_player_list, player_bye)
    return sorted_player_list


def remove_player_from_list(players_list: list, player_to_remove: str) -> list:
    return [player for player in players_list if player.get('Name') != player_to_remove]


def create_pairings_for_new_round(path_to_folder: Path, filename_of_parings: str, players: list) -> list:
    existing_pairings = read_pairings(path_to_folder, filename_of_parings)
    new_pairings = []
    while players:
        player = players.pop(0)
        for opponent in players:
            new_pair = {player.get('Name'), opponent.get('Name')}
            if new_pair not in existing_pairings and new_pair not in new_pairings:
                new_pairings.append(new_pair)
                players = remove_player_from_list(players, opponent.get('Name'))
                add_pairing(path_to_folder, filename_of_parings, player.get('Name'), opponent.get('Name'))
                break
    return new_pairings


# initialize_player_table(PLAYERS, folder_path, file_name)
pp = pprint.PrettyPrinter()
tabelka = read_players_table(folder_path, file_name)
tabelka_1 = sort_players_and_remove_bye(folder_path, file_name, None)
# tabelka_2 = sort_players_and_remove_bye(folder_path, file_name, Sitarski)

paringi_1 = create_pairings_for_new_round(folder_path, pairing_file, tabelka_1)
pp.pprint(paringi_1)
# paringi_2 = create_pairings_for_new_round(folder_path, pairing_file, tabelka_2)
# pp.pprint(paringi_2)

# add_pairing(folder_path, pairing_file, Dareczek, Rakos),
# add_pairing(folder_path, pairing_file, Stepien, Pasnik),
# add_pairing(folder_path, pairing_file, Kosma, Sitarski),
# add_pairing(folder_path, pairing_file, Krzywka, ABorowski),
# add_pairing(folder_path, pairing_file, Wirecki, Wytrych),
# add_pairing(folder_path, pairing_file, MBorowski, Sekula),
# add_pairing(folder_path, pairing_file, Podsiadlo, Pasnik),
# add_pairing(folder_path, pairing_file, ABorowski, Stepien),
# add_pairing(folder_path, pairing_file, MBorowski, Kosma),
# add_pairing(folder_path, pairing_file, Dareczek, Sekula),
# add_pairing(folder_path, pairing_file, Sitarski, Wytrych),
# add_pairing(folder_path, pairing_file, Dareczek, Wirecki),


# qwe = sort_players_and_remove_bye(folder_path, file_name, Rakos)
# asd = create_pairings_for_new_round(folder_path, pairing_file, qwe)
# print(asd)