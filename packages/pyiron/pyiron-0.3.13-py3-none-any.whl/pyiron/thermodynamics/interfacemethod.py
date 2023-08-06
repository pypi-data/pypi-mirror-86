# coding: utf-8
# Copyright (c) Max-Planck-Institut für Eisenforschung GmbH - Computational Materials Design (CM) Department
# Distributed under the terms of "New BSD License", see the LICENSE file.

import json
import numpy as np
import operator
import os
import matplotlib.pylab as plt
import random
from sklearn.neighbors.kde import KernelDensity

__author__ = "Lifang Zhu, Jan Janssen"
__copyright__ = "Copyright 2020, Max-Planck-Institut für Eisenforschung GmbH " \
                "- Computational Materials Design (CM) Department"
__version__ = "1.0"
__maintainer__ = "Jan Janssen"
__email__ = "janssen@mpie.de"
__status__ = "development"
__date__ = "Apr 24, 2020"


def freeze_one_half(basis):
    basis.add_tag(selective_dynamics=None)
    _, _, z = basis.scaled_pos_xyz()
    for selector, ind in zip(z < 0.5, range(len(basis))):
        if selector:
            basis.selective_dynamics[ind] = [True, True, True]
        else:
            basis.selective_dynamics[ind] = [False, False, False]
    return basis


def remove_selective_dynamics(basis):
    if 'selective_dynamics' in basis._tag_list.keys():
        for ind in range(len(basis)):
            basis.selective_dynamics[ind] = [True, True, True]
    return basis


def set_server(job, project_parameter):
    job.potential = project_parameter['potential']
    if 'queue' in project_parameter.keys():
        job.server.queue = project_parameter['queue']
    job.server.cores = project_parameter['cpu_cores']
    return job


def create_job_template(job_name, structure, project_parameter):
    pr = project_parameter['project']
    job = pr.create_job(project_parameter['job_type'], job_name)
    job.structure = structure
    return set_server(job=job, project_parameter=project_parameter)


def fix_iso(job):
    job.input.control['fix___ensemble'] = job.input.control['fix___ensemble'] + ' couple xyz'
    return job


def fix_z_dir(job):
    job.input.control['fix___ensemble'] = \
        job.input.control['fix___ensemble'].replace('x 0.0 0.0 1.0 y 0.0 0.0 1.0 z 0.0 0.0 1.0', 'z 0.0 0.0 1.0')
    return job


def half_velocity(job, temperature):
    job.input.control['velocity'] = job.input.control['velocity'].replace(str(temperature * 2), str(temperature))
    return job


def minimize_pos(structure, project_parameter, max_iter=1000):
    ham_minimize_pos = create_job_template(
        job_name='minimize_pos',
        structure=structure,
        project_parameter=project_parameter
    )
    ham_minimize_pos.calc_minimize(
        max_iter=max_iter,
        e_tol=1.0e-9,
        f_tol=1.0e-8,
        n_print=max_iter
    )
    ham_minimize_pos.run()
    ham_minimize_pos.project.wait_for_job(
        ham_minimize_pos,
        interval_in_s=100,
        max_iterations=100000
    )
    return ham_minimize_pos


def minimize_vol(structure, project_parameter, max_iter=1000):
    ham_minimize_vol = create_job_template(
        job_name='minimize_vol',
        structure=structure,
        project_parameter=project_parameter
    )
    ham_minimize_vol.calc_minimize(
        max_iter=max_iter,
        e_tol=1.0e-9,
        f_tol=1.0e-8,
        pressure=0.0,
        n_print=max_iter
    )
    ham_minimize_vol.input.control['fix___ensemble'] += ' vmax 0.001'
    ham_minimize_vol.run()
    ham_minimize_vol.project.wait_for_job(
        ham_minimize_vol,
        interval_in_s=100,
        max_iterations=100000
    )
    return ham_minimize_vol


def next_calc(structure, temperature, project_parameter, run_time_steps=10000):
    ham_temp = create_job_template(
        job_name='temp_heating_' + str(temperature).replace('.', '_'),
        structure=structure,
        project_parameter=project_parameter
    )
    ham_temp.calc_md(
        temperature=temperature,
        temperature_damping_timescale=100.0,
        pressure=0.0,
        pressure_damping_timescale=1000.0,
        n_print=run_time_steps,
        n_ionic_steps=run_time_steps,
        seed=project_parameter['seed'],
    )
    ham_temp = fix_iso(job=ham_temp)
    ham_temp = half_velocity(
        job=ham_temp,
        temperature=temperature
    )
    ham_temp.run()
    ham_temp.project.wait_for_job(
        ham_temp,
        interval_in_s=100,
        max_iterations=100000
    )
    return ham_temp.get_structure()


def npt_solid(temperature, basis, project_parameter, timestep=1.0):
    ham_npt_solid = create_job_template(
        job_name='ham_npt_solid_' + str(temperature).replace('.', '_'),
        structure=basis,
        project_parameter=project_parameter
    )
    ham_npt_solid.calc_md(
        temperature=temperature,
        temperature_damping_timescale=100.0,
        time_step=timestep,
        pressure=0.0,
        pressure_damping_timescale=1000.0,
        n_print=project_parameter['run_time_steps'],
        n_ionic_steps=project_parameter['run_time_steps'],
        seed=project_parameter['seed'],
    )
    ham_npt_solid = half_velocity(
        job=ham_npt_solid,
        temperature=temperature
    )
    ham_npt_solid = fix_iso(job=ham_npt_solid)
    ham_npt_solid.run()
    ham_npt_solid.project.wait_for_job(
        ham_npt_solid,
        interval_in_s=100,
        max_iterations=100000
    )
    return ham_npt_solid


def setup_liquid_job(job_name, basis, temperature, project_parameter, timestep=1.0):
    ham_npt_liquid_high = create_job_template(
        job_name=job_name,
        structure=freeze_one_half(basis),
        project_parameter=project_parameter
    )
    ham_npt_liquid_high.calc_md(
        temperature=temperature,
        temperature_damping_timescale=100.0,
        time_step=timestep,
        pressure=0.0,
        pressure_damping_timescale=1000.0,
        n_print=project_parameter['run_time_steps'],
        n_ionic_steps=project_parameter['run_time_steps'],
        seed=project_parameter['seed'],
    )
    ham_npt_liquid_high = half_velocity(
        job=ham_npt_liquid_high,
        temperature=temperature
    )
    ham_npt_liquid_high = fix_z_dir(
        job=ham_npt_liquid_high
    )
    ham_npt_liquid_high.run()
    ham_npt_liquid_high.project.wait_for_job(
        ham_npt_liquid_high,
        interval_in_s=100,
        max_iterations=100000
    )
    return ham_npt_liquid_high


def npt_liquid(temperature_solid, temperature_liquid, basis, project_parameter, timestep=1.0):
    ham_npt_liquid_high = setup_liquid_job(
        job_name='ham_npt_liquid_high_' + str(temperature_liquid).replace('.', '_'),
        basis=basis,
        temperature=temperature_liquid,
        project_parameter=project_parameter,
        timestep=timestep
    )
    ham_npt_liquid_low = setup_liquid_job(
        job_name='ham_npt_liquid_low_' + str(temperature_solid).replace('.', '_'),
        basis=ham_npt_liquid_high.get_structure(iteration_step=-1),
        temperature=temperature_solid,
        project_parameter=project_parameter,
        timestep=timestep
    )
    return ham_npt_liquid_low


def next_step_funct(number_of_atoms,
                    key_max,
                    structure_left,
                    structure_right,
                    temperature_left,
                    temperature_right,
                    distribution_initial_half,
                    structure_after_minimization,
                    run_time_steps,
                    project_parameter):
    structure_left_dict = structure_left.analyse_ovito_cna_adaptive()
    structure_right_dict = structure_right.analyse_ovito_cna_adaptive()
    temperature_diff = temperature_right - temperature_left
    if structure_left_dict[key_max] / number_of_atoms > distribution_initial_half and \
            structure_right_dict[key_max] / number_of_atoms > distribution_initial_half:
        structure_left = structure_right.copy()
        temperature_left = temperature_right
        temperature_right += temperature_diff
        structure_right = next_calc(
            structure=structure_after_minimization,
            temperature=temperature_right,
            project_parameter=project_parameter,
            run_time_steps=run_time_steps
        )
    elif structure_left_dict[key_max] / number_of_atoms > distribution_initial_half > \
            structure_right_dict[key_max] / number_of_atoms:
        temperature_diff /= 2
        temperature_left += temperature_diff
        structure_left = next_calc(
            structure=structure_after_minimization,
            temperature=temperature_left,
            project_parameter=project_parameter,
            run_time_steps=run_time_steps
        )
    elif structure_left_dict[key_max] / number_of_atoms < distribution_initial_half and \
            structure_right_dict[key_max] / number_of_atoms < distribution_initial_half:
        temperature_diff /= 2
        temperature_right = temperature_left
        temperature_left -= temperature_diff
        structure_right = structure_left.copy()
        structure_left = next_calc(
            structure=structure_after_minimization,
            temperature=temperature_left,
            project_parameter=project_parameter,
            run_time_steps=run_time_steps
        )
    else:
        raise ValueError('We should never reach this point!')
    return structure_left, structure_right, temperature_left, temperature_right


def round_temperature_next(temperature_next):
    return np.round(temperature_next, 2)


def strain_circle(basis_relative, temperature_next, nve_run_time_steps, project_parameter, timestep=1.0,
                  strain_result_lst=None, pressure_result_lst=None, center=None, fit_range=0.02):
    strain_lst, pressure_lst, temperature_lst, pressure_std_lst, temperature_std_lst = [], [], [], [], []
    ovito_dict_lst, ham_nvt_lst, ham_nve_lst = [], [], []
    strain_value_lst = get_strain_lst(
        fit_range=fit_range,
        points=project_parameter['points'],
        strain_result_lst=strain_result_lst,
        pressure_result_lst=pressure_result_lst,
        center=center
    )
    temperature_next = round_temperature_next(temperature_next)
    for strain in strain_value_lst:
        job_name = get_nve_job_name(
            temperature_next=temperature_next,
            strain=strain,
            steps_lst=project_parameter['nve_run_time_steps_lst'],
            nve_run_time_steps=nve_run_time_steps
        )
        ham_nve = project_parameter['project'].load(job_name)
        if ham_nve is None:
            basis_strain = basis_relative.copy()
            cell = basis_strain.cell.copy()
            cell[2, 2] *= strain
            basis_strain.set_cell(cell=cell, scale_atoms=True)
            ham_nvt = create_job_template(job_name=job_name.replace('nve', 'nvt'),
                                          structure=basis_strain,
                                          project_parameter=project_parameter)
            ham_nvt.calc_md(
                temperature=temperature_next,
                time_step=timestep,
                temperature_damping_timescale=100.0,
                n_print=project_parameter['nvt_run_time_steps'],
                n_ionic_steps=project_parameter['nvt_run_time_steps'],
                seed=project_parameter['seed'],
            )
            ham_nvt.input.control['fix___ensemble'] += ' drag 1'
            ham_nvt = half_velocity(
                job=ham_nvt,
                temperature=temperature_next
            )
            ham_nvt.write_restart_file()
            ham_nvt.run()
            ham_nvt_lst.append(ham_nvt)
    for ham_nvt in ham_nvt_lst:
        ham_nvt.project.wait_for_job(
            ham_nvt,
            interval_in_s=100,
            max_iterations=100000
        )
        ham_nve = ham_nvt.restart()
        ham_nve.job_name = ham_nvt.job_name.replace('nvt', 'nve')
        ham_nve.calc_md(
            n_ionic_steps=nve_run_time_steps,
            time_step=timestep,
            n_print=nve_run_time_steps / 100,
            seed=project_parameter['seed'],
        )
        ham_nve = set_server(
            job=ham_nve,
            project_parameter=project_parameter
        )
        ham_nve.input.control['dump___1'] = \
            ham_nve.input.control['dump___1'].replace('${dumptime}', str(nve_run_time_steps))
        ham_nve.run()
        ham_nve_lst.append(ham_nve)
    for ham_nve in ham_nve_lst:
        ham_nve.project.wait_for_job(
            ham_nve,
            interval_in_s=100,
            max_iterations=100000
        )
    for strain in strain_value_lst:
        job_name = get_nve_job_name(
            temperature_next=temperature_next,
            strain=strain,
            steps_lst=project_parameter['nve_run_time_steps_lst'],
            nve_run_time_steps=nve_run_time_steps
        )
        ham_nve = project_parameter['project'].load(job_name)
        press, temperature, press_std, temperature_std, ovito_dict = [
            np.mean(get_press(ham=ham_nve, step=-20)),
            np.mean(ham_nve['output/generic/temperature'][-20:]),
            np.std(get_press(ham=ham_nve, step=-20)),
            np.std(ham_nve['output/generic/temperature'][-20:]),
            ham_nve.get_structure(iteration_step=-1).analyse_ovito_cna_adaptive()
        ]
        strain_lst.append(strain)
        pressure_lst.append(press)
        temperature_lst.append(temperature)
        pressure_std_lst.append(press_std)
        temperature_std_lst.append(temperature_std)
        ovito_dict_lst.append(ovito_dict)
    return strain_lst, pressure_lst, temperature_lst, pressure_std_lst, temperature_std_lst, ovito_dict_lst


def analyse_minimized_structure(ham):
    final_structure = ham.get_structure(
        iteration_step=-1
    )
    final_structure_dict = final_structure.analyse_ovito_cna_adaptive()
    key_max = max(final_structure_dict.items(), key=operator.itemgetter(1))[0]
    number_of_atoms = len(final_structure)
    distribution_initial = final_structure_dict[key_max] / number_of_atoms
    distribution_initial_half = distribution_initial / 2
    return final_structure, key_max, number_of_atoms, distribution_initial_half, final_structure_dict


def get_press(ham, step=20):
    return np.mean(ham['output/generic/pressures'][step:, :, :].diagonal(0, 2), axis=1)


def get_center_point(strain_result_lst=None, pressure_result_lst=None, center=None):
    if strain_result_lst is not None and len(strain_result_lst) != 0 and \
            pressure_result_lst is not None and len(pressure_result_lst) != 0:
        center_point = np.round(np.roots(np.polyfit(strain_result_lst, pressure_result_lst, 1))[0], 2)
    elif center is not None:
        center_point = center
    else:
        center_point = 1.0
    return center_point


def get_strain_lst(fit_range=0.02, points=21, strain_result_lst=None, pressure_result_lst=None, center=None):
    center_point = get_center_point(
        strain_result_lst=strain_result_lst,
        pressure_result_lst=pressure_result_lst,
        center=center
    )
    return [np.round(s, 3) for s in np.linspace(center_point-fit_range, center_point+fit_range, points)]


def get_nve_job_name(temperature_next, strain, steps_lst, nve_run_time_steps):
    temperature_next = round_temperature_next(temperature_next)
    temp_str = str(temperature_next).replace('.', '_')
    strain_str = str(strain).replace('.', '_')
    steps_str = str(steps_lst.index(nve_run_time_steps))
    return 'ham_nve_' + strain_str + '_' + temp_str + '_' + steps_str


def plot_solid_liquid_ratio(temperature_next, strain_lst, nve_run_time_steps, project_parameter, debug_plot=True):
    cna_str = project_parameter['crystalstructure'].upper()
    ratio_lst = []
    for strain in strain_lst:
        job_name = get_nve_job_name(
            temperature_next=temperature_next,
            strain=strain,
            steps_lst=project_parameter['nve_run_time_steps_lst'],
            nve_run_time_steps=nve_run_time_steps
        )
        ham_nve = project_parameter['project'].load(job_name)
        struct = ham_nve.get_structure().center_coordinates_in_unit_cell()
        cna = struct.analyse_ovito_cna_adaptive(mode='str')
        bcc_count = sum(cna == 'BCC')
        fcc_count = sum(cna == 'FCC')
        hcp_count = sum(cna == 'HCP')
        if (cna_str == 'BCC' and bcc_count > fcc_count and bcc_count > hcp_count) or \
                (cna_str == 'FCC' and fcc_count > bcc_count and fcc_count > hcp_count) or \
                (cna_str == 'HCP' and hcp_count > bcc_count and hcp_count > fcc_count):
            # plt.figure(figsize=(16,12))
            bandwidth = (struct.get_volume()/len(struct))**(1.0/3.0)
            kde = KernelDensity(kernel='gaussian',
                                bandwidth=bandwidth).fit(struct.positions[:, 2][cna == cna_str].reshape(-1, 1))
            z_range = np.linspace(struct.positions[:, 2].min(), struct.positions[:, 2].max(), 1000)
            sample = kde.score_samples(z_range.reshape(-1, 1))
            gaussian_funct = np.exp(sample)/np.exp(sample).max()
            z_range_above_limit = z_range[np.where(gaussian_funct > 0.1)]
            z_range_below_limit = z_range[np.where(gaussian_funct < 0.1)]
            if len(z_range_above_limit) != 0:
                ratio_above = (np.max(z_range_above_limit)-np.min(z_range_above_limit)) / \
                              (np.max(z_range)-np.min(z_range))
            else:
                ratio_above = 1.0
            if len(z_range_below_limit) != 0:
                ratio_below = 1 - (np.max(z_range_below_limit)-np.min(z_range_below_limit)) / \
                              (np.max(z_range)-np.min(z_range))
            else:
                ratio_below = 0.0
            if ratio_below == 0.0:
                ratio = ratio_above
            elif ratio_above == 1.0:
                ratio = ratio_below
            else:
                ratio = np.min([ratio_below, ratio_above])
            ratio_lst.append(ratio)
        else:
            z_range = None
            gaussian_funct = None
            z_range_above_limit = None
            ratio = None
            ratio_lst.append(0.0)
        if debug_plot:
            plt.title('strain: ' + str(strain))
            plt.xlabel('position z')
            plt.ylabel('position x')
            plt.plot(struct.positions[:, 2], struct.positions[:, 0], 'o', label='all')
            plt.plot(struct.positions[:, 2][cna == 'BCC'], struct.positions[:, 0][cna == 'BCC'], 'x', label='BCC')
            plt.plot(struct.positions[:, 2][cna == 'FCC'], struct.positions[:, 0][cna == 'FCC'], 'x', label='FCC')
            plt.plot(struct.positions[:, 2][cna == 'HCP'], struct.positions[:, 0][cna == 'HCP'], 'x', label='HCP')
            cna_str_lst = struct.positions[:, 2][cna == cna_str]
            if len(cna_str_lst) != 0:
                plt.axvline(cna_str_lst.max(), color='red')
                plt.axvline(cna_str_lst.min(), color='red')
            plt.legend()
            plt.show()
            plt.xlabel('Position in z')
            plt.ylabel('kernel density score')
            plt.title('strain: ' + str(strain))
            if z_range is not None:
                plt.plot(z_range, gaussian_funct, label=cna_str)
                plt.axvline(np.min(z_range_above_limit), color='black', linestyle='--', label='ratio: ' + str(ratio))
                plt.axvline(np.max(z_range_above_limit), color='black', linestyle='--')
            plt.axhline(0.1, color='red')
            plt.legend()
            plt.show()
    return ratio_lst


def ratio_selection(strain_lst, ratio_lst, pressure_lst, temperature_lst, ratio_boundary, debug_plot=True):
    if debug_plot:
        plt.plot(strain_lst, ratio_lst)
        plt.axhline(0.5 + ratio_boundary, color='red', linestyle='--')
        plt.axhline(0.5, color='black', linestyle='--')
        plt.axhline(0.5 - ratio_boundary, color='red', linestyle='--')
        plt.xlabel('Strain')
        plt.ylabel('ratio solid vs. liquid')
    rat_lst, rat_col_lst = [], []
    for rat in ratio_lst:
        if (0.5 - ratio_boundary) < rat < (0.5 + ratio_boundary):
            rat_lst.append(rat)
        elif len(rat_lst) != 0:
            rat_col_lst.append(rat_lst)
            rat_lst = []
    if len(rat_lst) != 0:
        rat_col_lst.append(rat_lst)
    if len(rat_col_lst) != 0:
        rat_max_ind = np.argmax([len(l) for l in rat_col_lst])
        ratio_ind = [r in rat_col_lst[rat_max_ind] for r in ratio_lst]
        strain_value_lst = np.array(strain_lst)[ratio_ind]
        ratio_value_lst = np.array(ratio_lst)[ratio_ind]
        pressure_value_lst = np.array(pressure_lst)[ratio_ind]
        temperature_value_lst = np.array(temperature_lst)[ratio_ind]
        if debug_plot:
            plt.axvline(np.min(strain_value_lst), color='blue', linestyle='--')
            plt.axvline(np.max(strain_value_lst), color='blue', linestyle='--')
            plt.show()
        return strain_value_lst, ratio_value_lst, pressure_value_lst, temperature_value_lst, None
    else:
        if np.mean(ratio_lst) > 0.5:
            return [], [], [], [], 1
        else:
            return [], [], [], [], -1


def plot_equilibration(temperature_next, strain_lst, nve_run_time_steps, project_parameter, debug_plot=True):
    if debug_plot:
        for strain in strain_lst:
            job_name = get_nve_job_name(
                temperature_next=temperature_next,
                strain=strain,
                steps_lst=project_parameter['nve_run_time_steps_lst'],
                nve_run_time_steps=nve_run_time_steps
            )
            ham_nve = project_parameter['project'].load(job_name)
            plt.plot(ham_nve['output/generic/temperature'], label='strain: ' + str(strain))
            plt.axhline(np.mean(ham_nve['output/generic/temperature'][-20:]), linestyle='--', color='red')
            plt.axvline(range(len(ham_nve['output/generic/temperature']))[-20], linestyle='--', color='black')
            plt.legend()
            plt.xlabel('timestep')
            plt.ylabel('Temperature K')
            plt.legend()
            plt.show()


def plot_melting_point_prediction(strain_value_lst, pressure_value_lst, temperature_value_lst, boundary_value=0.25,
                                  debug_plot=True):
    fit_press = np.poly1d(np.polyfit(strain_value_lst, pressure_value_lst, 1))
    fit_temp = np.poly1d(np.polyfit(strain_value_lst, temperature_value_lst, 1))
    fit_temp_from_press = np.poly1d(np.polyfit(pressure_value_lst, temperature_value_lst, 1))
    fit_combined = np.poly1d(np.polyfit(fit_press(strain_value_lst), fit_temp(strain_value_lst), 1))
    if debug_plot:
        plt.plot(strain_value_lst, pressure_value_lst, 'o', label='pressure (strain)')
        plt.plot(strain_value_lst, fit_press(strain_value_lst), label='fit')
        plt.xlabel('Strain')
        plt.ylabel('Pressure GPa')
        plt.legend()
        plt.show()
        plt.plot(strain_value_lst, temperature_value_lst, 'o', label='temperature (strain)')
        plt.plot(strain_value_lst, fit_temp(strain_value_lst), label='fit')
        plt.xlabel('Strain')
        plt.ylabel('Temperature K')
        plt.legend()
        plt.show()
        plt.plot(pressure_value_lst, temperature_value_lst, 'o', label='temperature (pressure)')
        plt.plot(pressure_value_lst, fit_temp_from_press(pressure_value_lst), label='fit direct')
        plt.plot(fit_press(strain_value_lst), fit_temp(strain_value_lst), label='combined fits')
        plt.xlabel('Pressure GPa')
        plt.ylabel('Temperature K')
        plt.legend()
        plt.show()
    print(fit_temp_from_press(0.0), fit_combined(0.0))
    temperature_mean = np.min(temperature_value_lst) + \
        (np.max(temperature_value_lst) - np.min(temperature_value_lst)) * 1 / 2
    temperature_left = np.min(temperature_value_lst) + \
        (np.max(temperature_value_lst) - np.min(temperature_value_lst)) * (1 / 2 - boundary_value)
    temperature_right = np.min(temperature_value_lst) + \
        (np.max(temperature_value_lst) - np.min(temperature_value_lst)) * (1 / 2 + boundary_value)
    temperature_next = fit_temp_from_press(0.0)
    return temperature_next, temperature_mean, temperature_left, temperature_right


def calc_temp_iteration(basis, temperature_next, project_parameter, timestep, nve_run_time_steps, fit_range, center,
                        debug_plot=True):
    temperature_next = round_temperature_next(temperature_next)
    ham_npt_solid = npt_solid(
        temperature=temperature_next,
        basis=basis,
        project_parameter=project_parameter,
        timestep=timestep
    )
    ham_npt_liquid_low = npt_liquid(
        temperature_solid=temperature_next,
        temperature_liquid=temperature_next + 1000,
        basis=ham_npt_solid.get_structure(),
        project_parameter=project_parameter,
        timestep=timestep
    )
    basis = ham_npt_liquid_low.get_structure()
    basis_no_selective = remove_selective_dynamics(basis)
    basis_relative = basis_no_selective.copy()
    strain_lst, pressure_lst, temperature_lst, _, _, _ = strain_circle(
        basis_relative=basis_relative,
        temperature_next=temperature_next,
        nve_run_time_steps=nve_run_time_steps,
        project_parameter=project_parameter,
        timestep=timestep,
        strain_result_lst=None,
        pressure_result_lst=None,
        center=center,
        fit_range=fit_range
    )
    ratio_lst = plot_solid_liquid_ratio(
        temperature_next=temperature_next,
        strain_lst=strain_lst,
        nve_run_time_steps=nve_run_time_steps,
        project_parameter=project_parameter,
        debug_plot=debug_plot
    )
    strain_value_lst, _, pressure_value_lst, temperature_value_lst, sl_flag = ratio_selection(
        strain_lst=strain_lst,
        ratio_lst=ratio_lst,
        pressure_lst=pressure_lst,
        temperature_lst=temperature_lst,
        ratio_boundary=project_parameter['ratio_boundary'],
        debug_plot=debug_plot
    )
    if len(strain_value_lst) > 2:
        plot_equilibration(
            temperature_next=temperature_next,
            strain_lst=strain_lst,
            nve_run_time_steps=nve_run_time_steps,
            project_parameter=project_parameter,
            debug_plot=debug_plot
        )
        ind = check_for_holes(
            temperature_next=temperature_next,
            strain_value_lst=strain_value_lst,
            nve_run_time_steps=nve_run_time_steps,
            project_parameter=project_parameter
        )
        strain_value_lst = np.array(strain_value_lst)[ind].tolist()
        pressure_value_lst = np.array(pressure_value_lst)[ind].tolist()
        temperature_value_lst = np.array(temperature_value_lst)[ind].tolist()
        temperature_next, temperature_mean, temperature_left, temperature_right = plot_melting_point_prediction(
            strain_value_lst=strain_value_lst,
            pressure_value_lst=pressure_value_lst,
            temperature_value_lst=temperature_value_lst,
            boundary_value=project_parameter['boundary_value'],
            debug_plot=True
        )
    else:
        if sl_flag < 0:
            temperature_next, temperature_mean, temperature_left, temperature_right = temperature_next * 0.95, 0.0, 0.0, 0.0
        else:
            temperature_next, temperature_mean, temperature_left, temperature_right = temperature_next * 1.05, 0.0, 0.0, 0.0
    return temperature_next, temperature_mean, temperature_left, temperature_right, strain_value_lst, pressure_value_lst


def get_initial_melting_temperature_guess(project_parameter, ham_minimize_vol, temperature_next=None):
    structure_after_minimization, key_max, number_of_atoms, distribution_initial_half, _ = analyse_minimized_structure(
        ham_minimize_vol
    )
    temperature_left = project_parameter['temperature_left']
    temperature_right = project_parameter['temperature_right']
    if temperature_next is None:
        structure_left = structure_after_minimization
        structure_right = next_calc(
            structure=structure_after_minimization,
            temperature=temperature_right,
            project_parameter=project_parameter,
            run_time_steps=project_parameter['strain_run_time_steps']
        )
        temperature_step = temperature_right - temperature_left
        while temperature_step > 10:
            structure_left, structure_right, temperature_left, temperature_right = next_step_funct(
                number_of_atoms=number_of_atoms,
                key_max=key_max,
                structure_left=structure_left,
                structure_right=structure_right,
                temperature_left=temperature_left,
                temperature_right=temperature_right,
                distribution_initial_half=distribution_initial_half,
                structure_after_minimization=structure_after_minimization,
                run_time_steps=project_parameter['strain_run_time_steps'],
                project_parameter=project_parameter)
            temperature_step = temperature_right - temperature_left
        temperature_next = int(round(temperature_left))
        return temperature_next, structure_left
    else:
        return temperature_next, ham_minimize_vol.get_structure()


def validate_convergence(pr, temperature_left, temperature_next, temperature_right, enable_iteration,
                         timestep_iter, timestep_lst, timestep, fit_range_iter, fit_range_lst, fit_range,
                         nve_run_time_steps_iter, nve_run_time_steps_lst, nve_run_time_steps,
                         strain_result_lst, pressure_result_lst, step_count, step_dict, boundary_value, ratio_boundary,
                         convergence_goal, output_file='melting.json'):
    if temperature_left < temperature_next < temperature_right and enable_iteration:
        timestep = next(timestep_iter)
        fit_range = next(fit_range_iter)
        nve_run_time_steps = next(nve_run_time_steps_iter)
    if timestep == timestep_lst[-1] and fit_range == fit_range_lst[-1] and nve_run_time_steps == nve_run_time_steps_lst[-1]:
        enable_iteration = False
    center = np.abs(get_center_point(
        strain_result_lst=strain_result_lst,
        pressure_result_lst=pressure_result_lst
    ))
    step_count += 1
    if step_count not in step_dict.keys():
        step_dict[step_count] = {'timestep': timestep,
                                 'fit_range': fit_range,
                                 'nve_run_time_steps': nve_run_time_steps,
                                 'boundary_value': boundary_value,
                                 'ratio_boundary': ratio_boundary,
                                 'temperature_next': temperature_next,
                                 'center': center}
        with open(output_file, 'w') as f:
            json.dump(step_dict, f)
    else:
        timestep = step_dict[step_count]['timestep']
        fit_range = step_dict[step_count]['fit_range']
        nve_run_time_steps = step_dict[step_count]['nve_run_time_steps']
        boundary_value = step_dict[step_count]['boundary_value']
        ratio_boundary = step_dict[step_count]['ratio_boundary']
        temperature_next = step_dict[step_count]['temperature_next']
        center = step_dict[step_count]['center']
    if np.abs(step_dict[step_count]['temperature_next'] - step_dict[step_count - 1][
            'temperature_next']) <= convergence_goal:
        convergence_goal_achieved = True
    else:
        convergence_goal_achieved = False
    return convergence_goal_achieved, enable_iteration, step_count, step_dict, timestep, fit_range, nve_run_time_steps, \
        boundary_value, ratio_boundary, temperature_next, center


def initialise_iterators(project_parameter):
    return iter(project_parameter['timestep_lst']), iter(project_parameter['fit_range_lst']), iter(project_parameter['nve_run_time_steps_lst'])


def get_voronoi_volume(temperature_next, strain_lst, nve_run_time_steps, project_parameter):
    max_lst, mean_lst = [], []
    for strain in strain_lst:
        job_name = get_nve_job_name(
            temperature_next=temperature_next,
            strain=strain,
            steps_lst=project_parameter['nve_run_time_steps_lst'],
            nve_run_time_steps=nve_run_time_steps
        )
        ham_nve = project_parameter['project'].load(job_name)
        structure_voronoi_lst = ham_nve.get_structure().analyse_ovito_voronoi_volume()
        max_lst.append(np.max(structure_voronoi_lst))
        mean_lst.append(np.mean(structure_voronoi_lst))
    return max_lst, mean_lst


def check_for_holes(temperature_next, strain_value_lst, nve_run_time_steps, project_parameter, debug_plot=True):
    max_lst, mean_lst = get_voronoi_volume(
        temperature_next=temperature_next,
        strain_lst=strain_value_lst,
        nve_run_time_steps=nve_run_time_steps,
        project_parameter=project_parameter
    )
    if debug_plot:
        plt.plot(strain_value_lst, mean_lst, label='mean')
        plt.plot(strain_value_lst, max_lst, label='max')
        plt.axhline(np.mean(mean_lst) * 2, color='black', linestyle='--')
        plt.legend()
        plt.xlabel('Strain')
        plt.ylabel('Voronoi Volume')
        plt.show()
    return np.array(max_lst) < np.mean(mean_lst) * 2


def generate_structure(project_parameter):
    if 'lattice_constant' in project_parameter.keys():
        basis = project_parameter['project'].create_structure(
            project_parameter['element'],
            project_parameter['crystalstructure'].lower(),
            project_parameter['lattice_constant']
        )
    else:
        basis = project_parameter['project'].create_ase_bulk(
            project_parameter['element'],
            project_parameter['crystalstructure'].lower(),
            cubic=True
        )
    basis_lst = [basis.repeat([i, i, i]) for i in range(5, 30)]
    basis = basis_lst[np.argmin([np.abs(len(b) - project_parameter['number_of_atoms'] / 2)
                                 for b in basis_lst])]
    return basis


def generate_random_seed(project_parameter):
    if 'seed' not in project_parameter.keys():
        project_parameter['seed'] = random.randint(0, 99999)
    return project_parameter
