assert __name__ == '__main__'
import os, sys
# simfempypath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(simfempypath)

import simfempy
from simfempy.meshes.hole import square as sqhole
import simfempy.meshes.testmeshes as testmeshes
import pygmsh
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- #
def main():
    problemdata = createData()
    mesh = createMesh()
    print(f"{mesh=}")
    heat = simfempy.applications.heat.Heat(mesh=mesh, problemdata=problemdata)
    heat.static()
    simfempy.meshes.plotmesh.meshWithBoundaries(heat.mesh)
    result = heat.static()
    print(f"{result.info['timer']}")
    print(f"postproc: {result.data['global']['postproc']}")
    simfempy.meshes.plotmesh.meshWithData(heat.mesh, data=result.data, title="Heat example")
    plt.show()

# ---------------------------------------------------------------- #
def createMesh(h=2):
    rect = [-1, 1, -1, 1]
    with pygmsh.geo.Geometry() as geom:
        holes = []
        holes.append(sqhole(geom, xc=0, yc=0, r=0.2, mesh_size=h, label="3000"))
        # holes.append(sqhole(geom, xc=-0.5, yc=-0.5, r=0.2, mesh_size=h, label="200", make_surface=True))
        p = geom.add_rectangle(*rect, z=0, mesh_size=h, holes=holes)
        geom.add_physical(p.surface, label="100")
        for i in range(len(p.lines)): geom.add_physical(p.lines[i], label=f"{1000 + i}")
        mesh = geom.generate_mesh()
    from simfempy.meshes.plotmesh import plotmeshWithNumbering
    plotmeshWithNumbering(mesh)
    return simfempy.meshes.simplexmesh.SimplexMesh(mesh=mesh)

# ---------------------------------------------------------------- #
def createData():
    data = simfempy.applications.problemdata.ProblemData()
    bdrycond =  data.bdrycond
    bdrycond.set("Robin", [1000])
    bdrycond.set("Dirichlet", [1001, 1003])
    bdrycond.set("Neumann", [1002, 3000, 3001, 3002, 3003])
    bdrycond.set("Neumann", [1002])
    bdrycond.fct[1002] = lambda x,y,z, nx, ny, nz: 0.01
    bdrycond.fct[1001] = bdrycond.fct[1003] = lambda x,y,z: 120
    bdrycond.fct[1000] = lambda x, y, z, nx, ny, nz: 100
    bdrycond.param[1000] = 100
    postproc = data.postproc
    postproc.type['bdrymean_low'] = "bdry_mean"
    postproc.color['bdrymean_low'] = [1000]
    postproc.type['bdrymean_up'] = "bdry_mean"
    postproc.color['bdrymean_up'] = [1002]
    postproc.type['fluxn'] = "bdry_nflux"
    postproc.color['fluxn'] = [1001, 1003]
    params = data.params
    params.set_scal_cells("kheat", [100], 0.001)
    # params.set_scal_cells("kheat", [200], 10.0)
    # alternative:
    # def kheat(label, x, y, z):
    #     if label==100: return 0.0001
    #     return 0.1*label
    # params.fct_glob["kheat"] = kheat
    return data


# ================================================================c#


main()