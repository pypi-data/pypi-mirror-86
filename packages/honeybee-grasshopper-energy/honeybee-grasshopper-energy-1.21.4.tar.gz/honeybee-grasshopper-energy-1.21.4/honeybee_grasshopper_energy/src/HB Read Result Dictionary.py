# Ladybug: A Plugin for Environmental Analysis (GPL)
# This file is part of Ladybug.
#
# Copyright (c) 2020, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Parse an .rdd file from an energy simulation to show all possible outputs that
can be requested from the simulation.
-

    Args:
        _rdd: Full path to a RDD file that was generated by EnergyPlus.
        keywords_: An optional list of keywords that will be used to filter
            the output names.
        join_words_: If False or None, this component will automatically split
            any strings of multiple keywords (spearated by spaces) into separate
            keywords for searching. This results in a greater liklihood of
            finding an item in the search but it may not be appropropriate for
            all cases. You may want to set it to True when you are searching for
            a specific phrase that includes spaces. (Default: False).
    
    Returns:
        outputs: A list of EnergyPlus output names as strings (eg. 'Surface Window
            System Solar Transmittance'). If no keywords are input, this will
            be a list of all possible outputs that can be requested from the
            simulation. Outputs can be requested from the simulation by plugging
            them into the output_names_ of the "HB Custom Simulation Output" component. 
"""

ghenv.Component.Name = 'HB Read Result Dictionary'
ghenv.Component.NickName = 'ReadRDD'
ghenv.Component.Message = '1.1.0'
ghenv.Component.Category = 'HB-Energy'
ghenv.Component.SubCategory = '6 :: Result'
ghenv.Component.AdditionalHelpFromDocStrings = '0'

try:  # import the honeybee-core dependencies
    from honeybee.search import filter_array_by_keywords
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:
    from honeybee_energy.result.rdd import RDD
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy:\n\t{}'.format(e))

try:
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    rdd_obj = RDD(_rdd)
    if len(keywords_) == 0:
        outputs = rdd_obj.output_names
    else:
        split_words = True if join_words_ is None else not join_words_
        outputs = filter_array_by_keywords(rdd_obj.output_names, keywords_, split_words)
