import xlrd


subjects = [
    "AS001",
    "AS002",
    "AS004",
    "AS005",
    "AS006",
    "AS007",
    "AS008",
    "AS009",
    "AS011",
]

# Now we delete channels that need deleting.
wb = xlrd.open_workbook("removal.xls", on_demand=True)
mod_subs = wb.sheet_names()  # Excel workbooks sheets correspond to subjects who need
# to be edited


check_dict = dict()

for ms in mod_subs:
    if ms in subjects:
        check_dict[ms] = dict()
        sheet = wb.sheet_by_name(ms)
        # Iterate from second row till end of rows
        for k in range(1, sheet.nrows):
            # Get what details help determine index in `all_data` of item to be modified
            part, activity, *rems = sheet.row_values(k)
            rampnum, *rem_channs = list(map(int, rems))
            if not "_".join((part, activity)) in check_dict[ms]:
                check_dict[ms]["_".join((part, activity))] = dict()
            check_dict[ms]["_".join((part, activity))][rampnum] = rem_channs
