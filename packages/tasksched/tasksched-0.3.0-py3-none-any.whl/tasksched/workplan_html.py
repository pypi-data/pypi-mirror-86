#!/usr/bin/env python3
#
# Copyright (C) 2020 Sébastien Helleu <flashcode@flashtux.org>
#
# This file is part of Tasksched.
#
# Tasksched is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Tasksched is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tasksched.  If not, see <https://www.gnu.org/licenses/>.

"""Export work plan to HTML."""

from jinja2 import Environment, FileSystemLoader
from itertools import cycle

import calendar
import datetime
import os

from tasksched.utils import (
    add_business_days,
    get_days,
    get_months,
)

__all__ = (
    'workplan_to_html',
)

COLORS = range(10)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def workplan_to_html(workplan, template_file='basic', css_file='dark'):
    """
    Export work plan to HTML.

    :param dict workplan: work plan
    :param str template: template name or path to HTML template file (jinja2)
    :param str css: theme (light/dark) or path to CSS file
    :rtype: str
    :return: work plan as HTML
    """
    project = workplan['workplan']['project']
    resources = workplan['workplan']['resources']
    tasks = workplan['workplan']['tasks']
    iter_color = cycle(COLORS)
    tasks_colors = {}
    for task in tasks:
        if task['id'] not in tasks_colors:
            tasks_colors[task['id']] = next(iter_color) + 1
    project_start = datetime.date.fromisoformat(project['start'])
    project_end = datetime.date.fromisoformat(project['end'])
    hdays = {
        datetime.date.fromisoformat(hday): None
        for hday in project['holidays']
    }
    view_start = project_start.replace(day=1)
    view_end = project_end.replace(
        day=calendar.monthrange(project_end.year, project_end.month)[1])
    view_days = get_days(view_start, view_end, hdays)
    view_months = get_months(view_days)
    days = get_days(datetime.date.fromisoformat(project['start']),
                    datetime.date.fromisoformat(project['end']))
    if not template_file.endswith('.html'):
        template_file = os.path.join(DATA_DIR, 'html', f'{template_file}.html')
    if not css_file.endswith('.css'):
        css_file = os.path.join(DATA_DIR, 'css', f'{css_file}.css')
    with open(css_file) as _file:
        css = _file.read().strip()
    css_tasks = []
    for i in COLORS:
        css_tasks.append(f"""
.task_color_{i + 1} {{
  background: var(--task-color-{i + 1});
}}""")
    css_tasks = '\n'.join(css_tasks)
    css_months = []
    index = 2
    for i, month in enumerate(view_months):
        css_months.append(f"""
.month{i + 1} {{
  grid-column: {index} / span {month[1]};
}}""")
        index += month[1]
    css_months = '\n'.join(css_months)
    css = f"""
:root {{
  --plan-days: {len(view_days)};
  --plan-resources: {len(resources)};
}}
{css_tasks}
{css_months}
{css}
"""
    for resource in resources:
        end = datetime.date.fromisoformat(resource['end'])
        index = 0
        view_assigned = {day: 0 for day in view_days}
        current_date = project_start
        for task in resource['assigned']:
            count = task['duration']
            if not view_days[current_date]:
                current_date = add_business_days(current_date, 1, hdays)
            while count > 0:
                view_assigned[current_date] = \
                    (f'task_color_{tasks_colors[task["task"]]}',
                     task['task'])
                if view_days[current_date]:
                    count -= 1
                current_date += datetime.timedelta(days=1)
        resource['view_assigned'] = view_assigned
    template_dir, filename = os.path.split(os.path.abspath(template_file))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(filename)
    result = template.render(workplan['workplan'], css=css, days=days,
                             view_start=view_start, view_end=view_end,
                             view_days=view_days, view_months=view_months,
                             holidays=project['holidays'])
    return result
    # legend = ['Legend:']
    # tasks_colors = {}
    # for task in tasks:
    #     if task['id'] not in tasks_colors:
    #         tasks_colors[task['id']] = next(iter_color)
    #     str_id = (color(task['id'], tasks_colors[task['id']])
    #               if use_colors else task['id'])
    #     legend.append(f'  Task {str_id}: {task["title"]}{color_reset} '
    #                   f'({task["duration"]}d, prio: {task["priority"]}, '
    #                   f'max res: {task["max_resources"]})')
    # text = f'{project["resources_usage"]:.2f}%'
    # res_usage = (color_pct(text, project['resources_usage'])
    #              if use_colors else text)
    # info = (f'Work plan: {project["start"]} to {project["end"]} '
    #         f'({project["duration"]}d), {res_usage} resources used')
    # rows = [info, '']
    # max_len_res = max(len(res['name']) for res in resources) + 2
    # if use_unicode:
    #     char1, char2 = '█', '▊'
    # else:
    #     char1, char2 = 'x', '|'
    # for res in resources:
    #     text = f'{res["usage"]:>3.0f}%'
    #     usage = color_pct(text, res['usage']) if use_colors else text
    #     chars = []
    #     for i, task_id in enumerate(res['assigned']):
    #         char = (
    #             char2 if i < res['duration'] - 1
    #             and res['assigned'][i + 1] != res['assigned'][i]
    #             else char1
    #         )
    #         chars.append(color(char, tasks_colors[task_id])
    #                      if use_colors else char)
    #     bar_resource = ''.join(chars)
    #     tasks = ', '.join(res['assigned_tasks'])
    #     filler = ' ' * (project['duration'] - res['duration'] + 2)
    #     rows.append(
    #         f'{res["name"]:>{max_len_res}} > {res["end"] or " "*10} '
    #         f'{res["duration"]:>3}d {usage} '
    #         f'{bar_resource}{color_reset}{filler}{tasks}'
    #     )
    # return '\n'.join([
    #     '\n'.join(legend),
    #     '',
    #     '\n'.join(rows),
    # ])
