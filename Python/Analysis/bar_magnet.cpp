#include <vector>
#include <iostream>
#include <math.h>

std::vector<float> GetBarMagnetField(float x, float y, float z,
    float M_0, float X_B, float Y_B, float Z_B) {

	/*
    Returns the magnetic field intensity vector (H_x, H_y, H_z) at a given point (x, y, z).
    Calculates for a cuboid-shaped bar magnet with its geometric centre at (0, 0, 0).
    The North and South poles are along the positive and negative y-axes respectively.
    NOTE: Undefined at the surfaces of the magnet.
    Equation source: https://aip.scitation.org/doi/full/10.1063/1.1883308; page 2; eq. 5-7.

    Inputs:
       
       `x, y, z`: position vector, relative to (0, 0, 0) as the geometric centre of the magnet, at which
        to calculate the magnetic flux density vector. Units: metre

        `M_0`: remanent magnetisation. Units: amps per metre

        `X_B, Y_B, Z_B`: half-dimensions of the magnet along the x, y, z axes. Units: metre
     
     Outputs:
     
        `(H_x, H_y, H_z)`: H-field vector attached to input point. Units: A/m
	Note: B = mu_0 * (H + M).
	*/

    float scale_factor = M_0 / (4 * 3.14159265359);
    float sum_x = 0;
    float sum_y = 0;
    float sum_z = 0;
    float H_x;
    float H_y;
    float H_z;

    for (int k = 1; k <= 2; k++) {
        for (int l = 1; l <= 2; l++) {
            for (int m = 1; m <= 2; m++) {

                int t = ((k + l + m) % 2 == 0) ? 1 : -1;
                float h_x = (k % 2 == 0) ? x + X_B : x - X_B;
                float h_y = (l % 2 == 0) ? y + Y_B : y - Y_B;
                float h_z = (m % 2 == 0) ? z + Z_B : z - Z_B;
                float s = sqrt(h_x * h_x + h_y * h_y + h_z * h_z);
                sum_x = sum_x + t * log(h_z + s);
                sum_y = sum_y + t * (h_x * h_y / (abs(h_x) * abs(h_y)))
                    * atan((abs(h_x) / abs(h_y)) * (h_z / s));
                sum_z = sum_z + t * log(h_x + s);
             }
        }
    }

    H_x = scale_factor * sum_x;
    H_y = -1 * scale_factor * sum_y;
    H_z = scale_factor * sum_z;

	return { H_x, H_y, H_z };
}

int main() {

    float x = 10;
    float y = 15;
    float z = 20;
    const float M_0 = 795774.715459;

    std::vector<float> field_strength = GetBarMagnetField(x, y, z, M_0, 8, 12, 4);
    std::cout << "Magnetic Field Intensity, H(x, y, z) [A/m]: " << std::endl;
    std::cout << field_strength[0] << ' ' << field_strength[1] << ' ' << field_strength[2] << std::endl;
}
