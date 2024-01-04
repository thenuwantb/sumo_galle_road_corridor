# Generate probe vehicle flows with the ability of changing parameters programatically

def create_probe_flows(file_path, sigma):

    with open(file_path, 'w') as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write(
            '<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n'
        )
        fh.write('\n')

        fh.write(
            '\t<vType id="gen_probe" vClass="passenger" \n'
            '\t\t\t length="4.2" maxSpeed="22.22" width="2.1" \n'
            '\t\t\t minGap="2" color="0,0,1" guiShape="passenger/sedan"\n '
            f'\t\t\t sigma= "{sigma}"/>\n'
        )

        fh.write('\n')

        fh.write(
            '\t<flow id="gen_probe_entire" begin="0" end="18000" '
            ' period="120" from="112446385#5" to="455043449" '
            ' type="gen_probe" '
            ' departLane="free" '
            ' departSpeed="max" '
            '/>'
        )

        fh.write('\n')
        fh.write('</additional>')


