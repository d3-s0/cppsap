#include <iostream>
#include <fstream>
#include "json.hpp"

using json = nlohmann::json;

int main () {

    // Read in input file
    std::ifstream file("input.json");
    json data = json::parse(file);
    std::cout << data << std::endl;
    
    // Dimensions
    json dimensions = data["Dimensions"];
    float ground_floor_area = dimensions["ground_floor_area"];
    float first_floor_area = dimensions["first_floor_area"];
    float ground_floor_storey_height = dimensions["ground_floor_storey_height"];
    float first_floor_storey_height = ground_floor_storey_height + 0.25; // RdSAP
    float TFA = ground_floor_area + first_floor_area;
    float DV = (ground_floor_area * ground_floor_storey_height) + (first_floor_area * first_floor_storey_height);

    // Ventilation rate
    

    // Heat losses

    // Water heating requirement

    // Internal gains

    // Solar gains

    // Mean Internal Temperature

    // Space heating requirement
    
    // Energy requirements

    // Annual totals

    // Fuel costs

    // CO2 Emissions


    return 0;
}