import math
import json
from pathlib import Path

class SAP:
    def __init__(self, input_file):
        self.inp_file =inp_file
        self._dimensions = self.inp_file['Zone']['ThermalZone']
        self._ventilation = self.inp_file['InfiltrationVentilation']

    def dimensions(self):
        self.TFA = (
            self._dimensions['ground_floor_area']
            + self._dimensions['first_floor_area']
        )
        self.DV = (
            self._dimensions['ground_floor_area'] 
            * self._dimensions['ground_floor_storey_height']
            + self._dimensions['first_floor_area']
            * self._dimensions['first_floor_storey_height']
            )
        print(f"Box 4 TFA: {self.TFA}")
        print(f"Box 5 Dwelling volume: {self.DV}")

    def infil_vent(self):
        open_chimneys = self._ventilation['open_chimneys'] * 80
        open_flues = self._ventilation['open_flues'] * 20
        ini_infiltration = (open_chimneys+open_flues)
        ini_infiltration_rate = ini_infiltration / self.DV

        if self._ventilation['type_test'] == "manual":
            storeys = 2
            construction = 'masonry'
            floor = 'unsealed'
            lobby = 0 # RdSAP - House, bungalow or park home: no
            proofing = 0.05 # If no draught lobby, enter 0.05, else enter 0
            additional = (storeys - 1) * 0.1 if storeys > 1 else 0
            structural = 0.25 if construction in ['steel', 'timber'] else 0.35

            # RdSAP - Age band of main dwelling A to E: unsealed. Age band of main dwelling F to L: sealed
            floor_infiltration = 0.2 if floor == 'unsealed' else 0.1 if floor == 'sealed' else 0
            lobby_infiltration = 0.05 if lobby == 0 else 0
            window_infiltration = 0.25 - (0.2 * proofing / 100)
            adjusted_infiltration = (
                ini_infiltration_rate
                + additional
                + structural
                + floor_infiltration
                + lobby_infiltration
                + window_infiltration
                )
        # elif 50 :
        #     adjusted_infiltration = (ap50 / 20) + infiltration_rate
        # elif 4:
        #     adjusted_infiltration = (0.263 * (ap4 ** 0.924)) + infiltration_rate

        
        shelter_factor = 1 - (0.075 * self._ventilation["sheltered_sides"])
        final_infiltration = adjusted_infiltration * shelter_factor

        final_infiltration = 2
        monthly_wind = [5.10, 5.00, 4.90, 4.40, 4.30, 3.80, 3.80, 3.70, 4.00, 4.30, 4.50, 4.70]
        wind_factors = [w/4 for w in monthly_wind]
        adjusted_monthly = [final_infiltration * wf for wf in wind_factors]
        self.effective_ach = adjusted_monthly

        # Mechanical ventilation
        effective_ach = []
        for monthly in adjusted_monthly:
            system = "natural"
            if system == 'mvhr':
                efficiency = 80
                ach = monthly + 0.5 * (1 - efficiency/100)
            elif system == 'balanced':
                ach = monthly + 0.5
            elif system == 'mechanical':
                ach = monthly + 0.5 if monthly < 0.25 else monthly + 0.25
            else:
                # natural
                ach = monthly if monthly >= 1 else 0.5 + (0.5 * monthly**2)
            effective_ach.append(ach)

        # Results
        print(f"Box 8 Initial infiltration rate: {ini_infiltration_rate:.2f} ACH")
        print(f"Box 18 Adjusted infiltration: {adjusted_infiltration:.2f} ACH")
        print(f"Box 21 With shelter factor: {final_infiltration:.2f} ACH")
        print(f"Box 25 Effective ach: {[round(x, 2) for x in effective_ach]} ACH")


    def calc(self):
        self.dimensions()
        self.infil_vent()

BASE_DIR = Path(__file__).resolve().parent
inp_file_path = BASE_DIR / "input.json"
with open(inp_file_path) as file:
    inp_file = json.load(file)

sap = SAP(inp_file)
sap.calc()