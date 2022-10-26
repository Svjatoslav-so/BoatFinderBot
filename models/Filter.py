
class Filter:
    @staticmethod
    def filter_to_dict(boat_filter: tuple) -> dict:
        filter_key_list = ["user_id", "filter_name", "boat_name", "min_price", "max_price", "location", "min_year",
                           "max_year", "min_length", "max_length", "min_draft", "max_draft", "hull_material",
                           "fuel_type", "category", "type"]
        filter_dict = {}
        for i in range(len(boat_filter)):
            if not (boat_filter[i] is None):
                filter_dict.update({filter_key_list[i]: boat_filter[i]})

        return filter_dict

    @staticmethod
    def show(boat_filter: dict) -> str:
        key = set(boat_filter.keys())
        key = key - {"user_id", "filter_name"}
        f_str = f"{boat_filter['filter_name'].upper()}\n" if 'filter_name' in boat_filter.keys() else ""
        for k in key:
            f_str += k.title().replace("_", " ")+": "+str(boat_filter[k])+"\n"
        return f_str
