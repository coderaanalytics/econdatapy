import json
import jwt
import pandas
import requests
import warnings
from datetime import datetime
from econdatapy import login, settings
from pytz import timezone

econdata_token = None

def dataset(id, **params):


    # Parameters ----

    global econdata_token
    id = id if isinstance(id, (list, tuple)) else [id]
    if "agencyid" in params:
        x = params["agencyid"]
        agencyid = x if isinstance(x, (list, tuple)) else [x]
    else:
        agencyid = ["ECONDATA"]
    if "version" in params:
        x = params["version"]
        version = x if isinstance(x, (list, tuple)) else [x]
    else:
        version = ["latest"]
    env = settings.EconData()


    # Fetch data set(s) ----

    print("Fetching dataset(s) - " + ", ".join(id) + "\n")
    if "file" in params:
        with open(params["file"]) as file:
            data_message = json.load(file)
        print("Data set(s) successfully retrieved from local storage.\n")
    else:
        if econdata_token is None:
            econdata_token = login.helper(env)
        else:
            payload = econdata_token.split(" ")
            token = jwt.decode(payload[1], options={"verify_signature": False})
            if(datetime.now() > datetime.fromtimestamp(token["exp"])):
                econdata_token = login.helper(env)
        requests.post(env.url + "/signin",
                      headers = {"authorization": econdata_token})
        query_params = {"agencyids": ",".join(agencyid),
                        "ids": ",".join(id),
                        "versions": ",".join(version)}
        response = requests.get(env.url + "/" + env.path + "/datasets",
                                params = query_params,
                                headers = {"authorization": econdata_token})
        if not response.ok:
            raise Exception(response.json())
        data_message = response.json()
    data_sets = data_message[1]["data-sets"]
    database = [process_dataset(env, x, params) for x in data_sets]
    if len(database) == 1:
        return database[0]
    else:
        return database

def process_dataset(env, x, params):
    if "file" in params:
        tmp_data_set = x[1]
    else:
        data_set_ref = "-".join([x[1]["agencyid"],
                                 x[1]["id"],
                                 x[1]["version"]])
        query_params = {}
        release = get_release(env, params, data_set_ref)
        if release:
            query_params["release"] = release
        if "series_key" in params:
            query_params["series-key"] = params["series_key"]
        tmp_data_set = get_data(env, data_set_ref, query_params)
    series = [process_series(x) for x in tmp_data_set.pop("series")]
    series_keys = [x.metadata["series-key"] for x in series]
    data_set = {"metadata": tmp_data_set,
                "data": dict(zip(series_keys, series))}
    return data_set

def get_release(env, params, ref):
    release = None
    if "release" not in params:
        release = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    else:
        candidate_release = params["release"]
        try:
            release = datetime.strptime(candidate_release,
                                                 "%Y-%m-%dT%H:%M:%S")
        except:
            if candidate_release == "unreleased":
                release = None
            elif candidate_release == "latest":
                release = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            else:
                response = requests.get(env.url + "/" + env.path + \
                                        "/datasets/" + ref + "/release",
                                        params = params,
                                        headers = {"authorization": econdata_token})
                if not response.ok:
                    raise Exception(response.json())
                data_message = response.json()
                if not len(data_message["releases"]) == 0:
                    index = [(lambda y: y["description"] == candidate_release)(x)
                             for x in data_message["releases"]].index(True)
                    x = data_message["releases"][index]["release"]
                    y = datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")
                    z = y.astimezone(timezone("Africa/Johannesburg"))
                    release = z.strftime("%Y-%m-%dT%H:%M:%S")
                else:
                  Exception("Data set has no historical releases, ",
                            "try: release = \"unreleased\"")
    return release

def get_data(env, ref, params, **kwargs):
    if "links" not in kwargs:
        response = requests.get(env.url + "/" + env.path + "/datasets/" + ref,
                                params = params,
                                headers = {"authorization": econdata_token})
        if response.ok:
            print("Processing data set: " + ref + "\n")
        else:
            raise Exception(response.json())
        links = response.links
        data_message = response.json()
        data_set = data_message[1]["data-sets"][0][1]
        if "next" not in response.links:
            return data_set
        else:
            return get_data(env, ref, params,
                            links = links, data_set = data_set)
    else:
        response = requests.get(env.url + "/" + kwargs["links"]["next"]["url"],
                                params = params,
                                headers = {"authorization": econdata_token})
        if response.ok:
            print("Processing data set: " + ref + "\n")
        else:
            raise Exception(response.json())
        links = response.links
        data_message = response.json()
        data_set = kwargs["data_set"]
        data_set["series"] = data_set["series"] + \
                data_message[1]["data-sets"][0][1]["series"]
        if "next" not in response.links:
            return data_set
        else:
            return get_data(env, ref, params,
                            links = links, data_set = data_set)

def process_series(x):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        series = pandas.DataFrame(x.pop("obs"))
        series.metadata = x
        return series
