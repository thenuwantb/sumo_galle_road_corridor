# Generate vehicle type distribution

def create_vtype_dist(file_path, sigma):
    with open(file_path, 'w') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write(
            '<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n'
        )
        fh.write('\n')

        fh.write('\t <vTypeDistribution id="typedist1">\n')

        fh.write(
            '\t\t <vType id="Car" vClass="passenger" \n'
            '\t\t\t guiShape="passenger/sedan" \n'
            '\t\t\t probability="0.3417" minGap="2" \n'
            '\t\t\t length="4.2" width="2.1" \n'
            '\t\t\t maxSpeed="22.22" \n'
            f'\t\t\t sigma="{sigma}"/> \n'
        )

        fh.write('\n')

        fh.write(
            '\t\t <vType id="Motor_Cycle" vClass="motorcycle" \n'
            '\t\t\t guiShape="motorcycle" \n'
            '\t\t\t probability="0.2091" minGap="1" \n'
            '\t\t\t length="2.0" width="0.9" \n'
            '\t\t\t maxSpeed="22.22" \n'
            f'\t\t\t sigma="{sigma}"/> \n'
        )

        fh.write('\n')

        fh.write(
            '\t\t <vType id="Van" vClass="passenger" \n'
            '\t\t\t guiShape="passenger/van" \n'
            '\t\t\t probability="0.1996" minGap="2" \n'
            '\t\t\t length="5.3" width="2.10" \n'
            '\t\t\t maxSpeed="19.44" \n'
            f'\t\t\t sigma="{sigma}"/> \n'
        )

        fh.write('\n')

        fh.write(
            '\t\t <vType id="3_Wheeler" vClass="passenger" \n'
            '\t\t\t guiShape="passenger/hatchback" \n'
            '\t\t\t probability="0.1986" minGap="1" \n'
            '\t\t\t length="2.55" width="1.5" \n'
            '\t\t\t maxSpeed="16.67" \n'
            f'\t\t\t sigma="{sigma}"/> \n'
        )

        fh.write('\n')

        fh.write(
            '\t\t <vType id="Goods_Vehicle" vClass="truck" \n'
            '\t\t\t guiShape="truck" \n'
            '\t\t\t probability="0.0493" minGap="2.5" \n'
            '\t\t\t length="6.25" width="2.35" \n'
            '\t\t\t maxSpeed="13.889" \n'
            f'\t\t\t sigma="{sigma}"/> \n'
        )

        fh.write('\n')

        fh.write(
            '\t\t <vType id="Multi_Axle" vClass="trailer" \n'
            '\t\t\t guiShape="truck/trailer" \n'
            '\t\t\t probability="0.0017" minGap="2.5" \n'
            '\t\t\t length="15.5" width="3.0" \n'
            '\t\t\t maxSpeed="11.11" \n'
            f'\t\t\t sigma="{sigma}"/> \n'
        )

        fh.write('\n')

        fh.write('\t </vTypeDistribution> \n')
        fh.write('</additional>')
