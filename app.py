import math

import streamlit as st

st.set_page_config(page_title='SE Lab', page_icon='🧮')

if 'KLOC' not in st.session_state:
    st.session_state['KLOC'] = 0

if 'MODE' not in st.session_state:
    st.session_state['MODE'] = 'Organic'

if 'EFFORT' not in st.session_state:
    st.session_state['EFFORT'] = 0

if 'NUM_OF_PEOPLE_NEEDED' not in st.session_state:
    st.session_state['NUM_OF_PEOPLE_NEEDED'] = 0

if 'NUM_OF_MONTHS_NEEDED' not in st.session_state:
    st.session_state['NUM_OF_MONTHS_NEEDED'] = 0

if 'n1' not in st.session_state:
    st.session_state['n1'] = 0

if 'n2' not in st.session_state:
    st.session_state['n2'] = 0

if 'N1' not in st.session_state:
    st.session_state['N1'] = 0

if 'N2' not in st.session_state:
    st.session_state['N2'] = 0

if 'program_length' not in st.session_state:
    st.session_state['program_length'] = 0

if 'program_vocabulary' not in st.session_state:
    st.session_state['program_vocabulary'] = 0

if 'program_volume' not in st.session_state:
    st.session_state['program_volume'] = 0

if 'program_difficulty' not in st.session_state:
    st.session_state['program_difficulty'] = 0

if 'program_level' not in st.session_state:
    st.session_state['program_level'] = 0

if 'program_effort' not in st.session_state:
    st.session_state['program_effort'] = 0

if 'program_time' not in st.session_state:
    st.session_state['program_time'] = 0

if 'program_bugs' not in st.session_state:
    st.session_state['program_bugs'] = 0


class HalsteadSoftwareMetrics:
    """
    Halstead Software Metrics
    This class contains the methods to calculate the program length, program vocabulary, program volume, program
    difficulty, program level, program effort, program time and program bugs
    """

    @staticmethod
    def invoke():
        HalsteadSoftwareMetrics.calculate_program_length()
        HalsteadSoftwareMetrics.calculate_program_vocabulary()
        HalsteadSoftwareMetrics.calculate_program_volume()
        HalsteadSoftwareMetrics.calculate_program_difficulty()
        HalsteadSoftwareMetrics.calculate_program_level()
        HalsteadSoftwareMetrics.calculate_program_effort()
        HalsteadSoftwareMetrics.calculate_program_time()
        HalsteadSoftwareMetrics.calculate_program_bugs()

    @staticmethod
    def calculate_program_length():
        st.session_state['program_length'] = st.session_state['N1'] + st.session_state['N2']

    @staticmethod
    def calculate_program_vocabulary():
        st.session_state['program_vocabulary'] = st.session_state['n1'] + st.session_state['n2']

    @staticmethod
    def calculate_program_volume():
        st.session_state['program_volume'] = round(st.session_state['program_length'] * math.log2(
            st.session_state['program_vocabulary']), 2)

    @staticmethod
    def calculate_program_difficulty():
        st.session_state['program_difficulty'] = (st.session_state['n1'] / 2) * (
                st.session_state['N1'] / st.session_state['n2'])

    @staticmethod
    def calculate_program_level():
        vs = (2 + st.session_state['n2']) * math.log2(2 + st.session_state['n2'])
        st.session_state['program_level'] = round(vs / st.session_state['program_volume'], 2)

    @staticmethod
    def calculate_program_effort():
        st.session_state['program_effort'] = st.session_state['program_difficulty'] * st.session_state['program_volume']

    @staticmethod
    def calculate_program_time():
        st.session_state['program_time'] = round((st.session_state['program_effort'] / 18), 2)

    @staticmethod
    def calculate_program_bugs():
        bug = st.session_state['program_volume'] / 3000
        st.session_state['program_bugs'] = round(bug, 2)


def on_change(kloc):
    st.session_state['KLOC'] = kloc


class BasicCocomoModel:
    """
    Basic Cocomo Model
    This class contains the methods to calculate the effort, number of months needed and number of people needed
    """

    @staticmethod
    def calculate_time():
        if st.session_state['MODE'] == 'Organic':
            st.session_state['NUM_OF_MONTHS_NEEDED'] = 2.5 * (st.session_state['EFFORT'] ** 0.38)
        elif st.session_state['MODE'] == 'Semi-detached':
            st.session_state['NUM_OF_MONTHS_NEEDED'] = 2.5 * (st.session_state['EFFORT'] ** 0.35)
        else:
            st.session_state['NUM_OF_MONTHS_NEEDED'] = 2.5 * (st.session_state['EFFORT'] ** 0.32)

    @staticmethod
    def calculate_average_staff_required():
        if st.session_state['NUM_OF_MONTHS_NEEDED'] == 0:
            st.error('Please enter the KLOC value')
            return
        st.session_state['NUM_OF_PEOPLE_NEEDED'] = st.session_state['EFFORT'] / st.session_state['NUM_OF_MONTHS_NEEDED']

    @staticmethod
    def calculate_effort():
        if st.session_state['MODE'] == 'Organic':
            st.session_state['EFFORT'] = 2.4 * (st.session_state['KLOC'] ** 1.05)
        elif st.session_state['MODE'] == 'Semi-detached':
            st.session_state['EFFORT'] = 3.0 * (st.session_state['KLOC'] ** 1.12)
        else:
            st.session_state['EFFORT'] = 3.6 * (st.session_state['KLOC'] ** 1.20)
        BasicCocomoModel.calculate_time()
        BasicCocomoModel.calculate_average_staff_required()


tab1, tab2 = st.tabs(['Basic Cocomo Model', 'Halstead\'s Software Metrics'])
with tab1:
    st.title('Basic Cocomo Model')
    st.subheader('Effort Estimation')
    st.text('Enter the values of the following parameters to get the effort estimation')
    value = st.text_input(label='KLOC', value='0', key='BasicKLOC')
    if value.isdigit():
        on_change(int(value))
    else:
        st.error('Please enter only integer value')
    st.text('Select the mode')
    mode = st.radio(label='Mode', options=['Organic', 'Semi-detached', 'Embedded'])
    st.session_state['MODE'] = mode  # Setting the mode in session state
    st.button(label='Estimate Effort', use_container_width=True, on_click=BasicCocomoModel.calculate_effort)
    st.subheader('Cost Estimation')
    st.success(f'Effort = {round(st.session_state["EFFORT"])} PM')
    st.success(f'Month Needed = {round(st.session_state['NUM_OF_MONTHS_NEEDED'])} Months')
    st.success(f'Number of People Needed = {round(st.session_state['NUM_OF_PEOPLE_NEEDED'])} Person')

with tab2:
    st.title('Halstead\'s Software Metrics')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Input')
        n1 = st.text_input(label='Num of unique operators n1', value='0')
        if n1.isdigit():
            st.session_state['n1'] = int(n1)
        else:
            st.error('Please enter only integer value')
        N1 = st.text_input(label='Num of occurrences operators N1', value='0')
        if N1.isdigit():
            st.session_state['N1'] = int(N1)
        else:
            st.error('Please enter only integer value')

        n2 = st.text_input(label='Num of unique operands n2', value='0')
        if n2.isdigit():
            st.session_state['n2'] = int(n2)
        else:
            st.error('Please enter only integer value')

        N2 = st.text_input(label='Num of occurrences operands N2', value='0')
        if N2.isdigit():
            st.session_state['N2'] = int(N2)
        else:
            st.error('Please enter only integer value')

        st.button(label='Calculate', use_container_width=True, on_click=HalsteadSoftwareMetrics.invoke)
        st.button(label='Balloons', use_container_width=True, on_click=lambda: st.balloons())
    with col2:
        st.subheader('Output')
        st.success(f'Program Length = {st.session_state["program_length"]}')
        st.success(f'Program Vocabulary = {st.session_state["program_vocabulary"]}')
        st.success(f'Program Volume = {st.session_state["program_volume"]}')
        st.success(f'Program Difficulty = {st.session_state["program_difficulty"]}')
        st.success(f'Program Level = {st.session_state["program_level"]}')
        st.success(f'Program Effort = {st.session_state["program_effort"]}')
        st.success(f'Program Time = {st.session_state["program_time"]}')
        st.success(f'Program Bugs = {st.session_state["program_bugs"]}')
