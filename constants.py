LABEL = "{quality} [{unit}]"
KILOGRAY_POT = 'kGy/POT'
PER_SQUARE_CM_POT = '1/(cm^2 * POT)'
CM = "cm"

flag_labels = ["Dose"]

y_labels = {
		"Dose": "Dose",
		"1MeVN": "1MeVN",
		"HEHeq": "HEHeq",
		"HEH": "HEH",
		"Neutron": "Neutron",
		"ThNeutron": "Thermal Neutron",
		"Proton": "Proton"
}

y_units = {
		"Dose": KILOGRAY_POT,
		"1MeVN": PER_SQUARE_CM_POT,
		"HEHeq": PER_SQUARE_CM_POT,
		"HEH": PER_SQUARE_CM_POT,
		"Neutron": PER_SQUARE_CM_POT,
		"ThNeutron": PER_SQUARE_CM_POT,
		"Proton": PER_SQUARE_CM_POT
}

x_labels = {
        "X": "X Axis",
        "Z": "Z Axis"
}

x_units = {
        "X": CM,
        "Z": CM
}
