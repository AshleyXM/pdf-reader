def generate_final_text(text_result, image_result=None):
    res = ""
    if image_result is not None:  # check the image result first, to avoid keeping checking in each loop
        for idx, text in enumerate(text_result, start=1):
            res += f"\nPage{idx}\n"  # add page header
            res += f"{text}\n"  # add page text content
            if idx in image_result:
                for alt_txt in image_result[idx]:
                    res += f"{alt_txt}\n"  # add page image alternative text
            res += "\n"  # add line space between pages
    else:
        for idx, text in enumerate(text_result, start=1):
            res += f"\nPage{idx}\n"  # add page header
            res += f"{text}\n"  # add page text content
            res += "\n"  # add line space between pages
    return res
