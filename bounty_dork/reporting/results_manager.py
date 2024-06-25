import csv
import json
import os
import sys

from termcolor import cprint

import threading

google_dorking_results = []


LOCKS = {
    "dorking": threading.Lock(),
}
#########################################################################################
# File writing functions
#########################################################################################

# Define file paths
# Initialize locks for thread-safe file writing
# TODO make more modular


def get_processed_dorks(settings):
    """
    Reads the experiment CSV file to get the list of processed dorks.
    """
    processed_dorks = set()

    if os.path.exists(settings["dorking_csv"]):
        with open(settings["dorking_csv"], mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                processed_dorks.add(row["dork"])

    return processed_dorks


def get_last_processed_ids(settings):
    """
    Get the last processed dork_id, link_id, and attack_id from the CSV file.
    """
    last_dork_id = 0
    last_link_id = 0
    last_attack_id = 0

    if os.path.exists(settings["dorking_csv"]):
        with open(settings["dorking_csv"], mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                last_dork_id = int(row["dork_id"])
                last_link_id = int(row["link_id"])
                last_attack_id = int(row["attack_id"])

    return last_dork_id, last_link_id, last_attack_id

# Thread-safe addition to results lists
def save_dorking_query(result, settings):
    """
    Safely adds results to the single experiment CSV file with tracking IDs.
    """
    dork_id, category, urls, dork = result
    with LOCKS["dorking"]:
        with open(settings["dorking_csv"], mode="a", newline="") as file:
            writer = csv.writer(file)
            _, link_id, last_attack_id = get_last_processed_ids(settings)
            link_id += 1  # Increment link_id for next link
            if urls:
                cprint(
                    f"Adding {len(urls)} URLs to experiment list...",
                    "blue",
                    file=sys.stderr,
                )
                for url in urls:
                    if url and "https://www.google.com/sorry/" not in url:
                        attack_id = (
                            last_attack_id  # Start attack_id from 1 for each link
                        )
                        row = [
                            dork_id,
                            link_id,
                            attack_id,
                            category,
                            url,
                            dork,
                            "yes",
                            "",
                        ]  # Success and payload columns are initially empty
                        # if settings["do_dorking_github"] and category == "github":
                        #     row.append("no")
                        writer.writerow(row)
                        cprint(
                            f"Added {url} to experiment list under category {category}",
                            "blue",
                            file=sys.stderr,
                        )
                        attack_id += 1  # Increment attack_id for next attack
                    else:
                        cprint(
                            f"Google blocked us from accessing {url}",
                            "red",
                            file=sys.stderr,
                        )
                link_id += 1  # Increment link_id for next link
            else:
                # Write a row indicating no URLs found for this dork
                row = [
                    dork_id,
                    link_id,
                    last_attack_id,
                    category,
                    "",
                    dork,
                    "no",
                    "",
                ]  # No URLs found
                # if settings["do_dorking_github"]:
                #     row.append("no")
                
                writer.writerow(row)
                cprint(f"No URLs found for {category} dorks...", "red", file=sys.stderr)
