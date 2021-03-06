#!/usr/bin/env python
'''XDMF generation for syntehtic data generator'''

from xml.dom.minidom import Document


class Xdmf(object):
    '''Class representing an XDMF data descriptor builder'''

    def __init__(self, centers,  particles, points, h5file_name):
        '''Constructor'''
        self._centers = centers
        self._particles = particles
        self._points = points
        self._h5 = h5file_name
        self._doc = Document()
        xdmf = self._doc.createElement('Xdmf')
        xdmf.setAttribute('xmlns:xi', 'http://www.w3.org/2001/XInclude')
        xdmf.setAttribute('Version', '2.0')
        self._doc.appendChild(xdmf)
        self._domain = self._doc.createElement('Domain')
        self._domain.setAttribute('Name', 'domain')
        xdmf.appendChild(self._domain)

    def to_xml(self, xml_file_name, indent='  '):
        with open(xml_file_name, 'w') as xml_file:
            xml_file.write(self._doc.toprettyxml(indent=indent))

    def create_centers(self):
        grid = self._doc.createElement('Grid')
        grid.setAttribute('Name', 'centers')
        grid.setAttribute('GridType', 'Uniform')
        self._domain.appendChild(grid)
        topology = self._doc.createElement('Topology')
        topology.setAttribute('Name', 'center_topology')
        topology.setAttribute('TopologyType', 'Polyvertex')
        grid.appendChild(topology)
        geometry = self._doc.createElement('Geometry')
        geometry.setAttribute('Name', 'center_geometry')
        geometry.setAttribute('GeometryType', 'XYZ')
        item = self._doc.createElement('DataItem')
        item.setAttribute('Format', 'HDF')
        item.setAttribute('DataType', 'Float')
        item.setAttribute('Precision', '8')
        item.setAttribute('Dimensions', '{0:d} 3'.format(self._centers))
        ref = self._doc.createTextNode(
            '{0}:/centers'.format(self._h5)
        )
        item.appendChild(ref)
        geometry.appendChild(item)
        grid.appendChild(geometry)
        attribute = self._doc.createElement('Attribute')
        attribute.setAttribute('Name', 'center weight')
        attribute.setAttribute('Center', 'Node')
        item = self._doc.createElement('DataItem')
        item.setAttribute('Format', 'XML')
        item.setAttribute('DataType', 'Float')
        item.setAttribute('Precision', '8')
        item.setAttribute('Dimensions', '{0:d}'.format(self._centers))
        ref = self._doc.createTextNode(
            ' '.join(['1.0']*self._centers)
        )
        item.appendChild(ref)
        attribute.appendChild(item)
        grid.appendChild(attribute)

    def create_particles(self):
        grid = self._doc.createElement('Grid')
        grid.setAttribute('Name', 'particles')
        grid.setAttribute('GridType', 'Uniform')
        self._domain.appendChild(grid)
        topology = self._doc.createElement('Topology')
        topology.setAttribute('Name', 'particle_topology')
        topology.setAttribute('TopologyType', 'Polyvertex')
        grid.appendChild(topology)
        geometry = self._doc.createElement('Geometry')
        geometry.setAttribute('Name', 'particle_geometry')
        geometry.setAttribute('GeometryType', 'XYZ')
        item = self._doc.createElement('DataItem')
        item.setAttribute('Format', 'HDF')
        item.setAttribute('DataType', 'Float')
        item.setAttribute('Precision', '8')
        item.setAttribute('Dimensions', '{0:d} 3'.format(self._particles))
        ref = self._doc.createTextNode(
            '{0}:/particles/position'.format(self._h5)
        )
        item.appendChild(ref)
        geometry.appendChild(item)
        grid.appendChild(geometry)
        attribute = self._doc.createElement('Attribute')
        attribute.setAttribute('Name', 'mass')
        attribute.setAttribute('Center', 'Node')
        item = self._doc.createElement('DataItem')
        item.setAttribute('Format', 'HDF')
        item.setAttribute('DataType', 'Float')
        item.setAttribute('Precision', '8')
        item.setAttribute('Dimensions', '{0:d}'.format(self._particles))
        ref = self._doc.createTextNode(
            '{0}:/particles/mass'.format(self._h5)
        )
        item.appendChild(ref)
        attribute.appendChild(item)
        grid.appendChild(attribute)
        attribute = self._doc.createElement('Attribute')
        attribute.setAttribute('Name', 'velocity')
        attribute.setAttribute('Center', 'Node')
        attribute.setAttribute('AttributeType', 'Vector')
        item = self._doc.createElement('DataItem')
        item.setAttribute('Format', 'HDF')
        item.setAttribute('DataType', 'Float')
        item.setAttribute('Precision', '8')
        item.setAttribute('Dimensions', '{0:d} 3'.format(self._particles))
        ref = self._doc.createTextNode(
            '{0}:/particles/velocity'.format(self._h5)
        )
        item.appendChild(ref)
        attribute.appendChild(item)
        grid.appendChild(attribute)

    def create_field_geometry(self):
        topology = self._doc.createElement('Topology')
        topology.setAttribute('Name', 'field_topology')
        topology.setAttribute('TopologyType', '3DRectMesh')
        topology.setAttribute('Dimensions',
                              '{0:d} {0:d} {0:d}'.format(self._points))
        self._domain.appendChild(topology)
        geometry = self._doc.createElement('Geometry')
        geometry.setAttribute('Name', 'field_geometry')
        geometry.setAttribute('GeometryType', 'VXVYVZ')
        self._domain.appendChild(geometry)
        for coord in "xyz":
            item = self._doc.createElement('DataItem')
            item.setAttribute('Name', coord)
            item.setAttribute('Format', 'HDF')
            item.setAttribute('DataType', 'Float')
            item.setAttribute('Precision', '8')
            item.setAttribute('Dimensions', str(self._points))
            array = self._doc.createTextNode(
                '{0}:/grid/{1}'.format(self._h5, coord)
            )
            item.appendChild(array)
            geometry.appendChild(item)

    def create_scalar_field(self):
        grid = self._doc.createElement('Grid')
        grid.setAttribute('Name', 'scalar_field')
        grid.setAttribute('GridType', 'Uniform')
        self._domain.appendChild(grid)
        topology = self._doc.createElement('Topology')
        topology.setAttribute('Reference', '/Xdmf/Domain/Topology[1]')
        grid.appendChild(topology)
        geometry = self._doc.createElement('Geometry')
        geometry.setAttribute('Reference', '/Xdmf/Domain/Geometry[1]')
        grid.appendChild(geometry)
        attribute = self._doc.createElement('Attribute')
        attribute.setAttribute('Name', 'scalar field')
        attribute.setAttribute('Center', 'Node')
        grid.appendChild(attribute)
        item = self._doc.createElement('DataItem')
        item.setAttribute('Format', 'HDF')
        item.setAttribute('DataType', 'Float')
        item.setAttribute('Precision', '8')
        item.setAttribute('Dimensions',
                          '{0:d} {0:d} {0:d}'.format(self._points))
        data = self._doc.createTextNode('{0}:/scalar'.format(self._h5))
        item.appendChild(data)
        attribute.appendChild(item)

    def create_vector_field(self):
        grid = self._doc.createElement('Grid')
        grid.setAttribute('GridType', 'Uniform')
        self._domain.appendChild(grid)
        topology = self._doc.createElement('Topology')
        topology.setAttribute('Reference', '/Xdmf/Domain/Topology[1]')
        grid.appendChild(topology)
        geometry = self._doc.createElement('Geometry')
        geometry.setAttribute('Reference', '/Xdmf/Domain/Geometry[1]')
        grid.appendChild(geometry)
        for dim in 'xyz':
            attribute = self._doc.createElement('Attribute')
            attribute.setAttribute('Name', '{0}-component'.format(dim))
            attribute.setAttribute('Center', 'Node')
            grid.appendChild(attribute)
            item = self._doc.createElement('DataItem')
            item.setAttribute('Format', 'HDF')
            item.setAttribute('DataType', 'Float')
            item.setAttribute('Precision', '8')
            item.setAttribute('Dimensions',
                              '{0:d} {0:d} {0:d}'.format(self._points))
            data = self._doc.createTextNode(
                '{0}:/vector/{1}'.format(self._h5, dim)
            )
            item.appendChild(data)
            attribute.appendChild(item)


if __name__ == '__main__':
    from argparse import ArgumentParser

    arg_parser = ArgumentParser(description='genearte XMDF file')
    arg_parser.add_argument('--h5', required=True, help='HDF5 data file')
    arg_parser.add_argument('--centers', type=int, default=5,
                            help='number of centers')
    arg_parser.add_argument('--particle_data', action='store_true',
                            help='generate XDMF for particle data')
    arg_parser.add_argument('--particles', type=int, default=50,
                            help='number of particles')
    arg_parser.add_argument('--scalar_field_data', action='store_true',
                            help='generate XDMF for scalar field data')
    arg_parser.add_argument('--vector_field_data', action='store_true',
                            help='generate XDMF for vector field data')
    arg_parser.add_argument('--points', type=int, default=100,
                            help='number of grid points for grid')
    arg_parser.add_argument('file', help='XDMF file name')
    options = arg_parser.parse_args()
    xdmf = Xdmf(options.centers, options.particles, options.points,
                options.h5)
    xdmf.create_centers()
    if options.particle_data:
        xdmf.create_particles()
    if options.scalar_field_data or options.vector_field_data:
        xdmf.create_field_geometry()
    if options.scalar_field_data:
        xdmf.create_scalar_field()
    if options.vector_field_data:
        xdmf.create_vector_field()
    xdmf.to_xml(options.file)
