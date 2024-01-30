import streamlit as st

st.set_page_config(page_title='Cocomo Model', page_icon=':shark:')

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


def on_change(kloc):
    st.session_state['KLOC'] = kloc


def calculate_time():
    if st.session_state['MODE'] == 'Organic':
        st.session_state['NUM_OF_MONTHS_NEEDED'] = 2.5 * (st.session_state['EFFORT'] ** 0.38)
    elif st.session_state['MODE'] == 'Semi-detached':
        st.session_state['NUM_OF_MONTHS_NEEDED'] = 2.5 * (st.session_state['EFFORT'] ** 0.35)
    else:
        st.session_state['NUM_OF_MONTHS_NEEDED'] = 2.5 * (st.session_state['EFFORT'] ** 0.32)


def calculate_average_staff_required():
    if st.session_state['NUM_OF_MONTHS_NEEDED'] == 0:
        st.error('Please enter the KLOC value')
        return
    st.session_state['NUM_OF_PEOPLE_NEEDED'] = st.session_state['EFFORT'] / st.session_state['NUM_OF_MONTHS_NEEDED']


def calculate_effort():
    if st.session_state['MODE'] == 'Organic':
        st.session_state['EFFORT'] = 2.4 * (st.session_state['KLOC'] ** 1.05)
    elif st.session_state['MODE'] == 'Semi-detached':
        st.session_state['EFFORT'] = 3.0 * (st.session_state['KLOC'] ** 1.12)
    else:
        st.session_state['EFFORT'] = 3.6 * (st.session_state['KLOC'] ** 1.20)
    calculate_time()
    calculate_average_staff_required()


with st.container():
    st.title('Cocomo Model')
    st.subheader('Effort Estimation')
    st.text('Enter the values of the following parameters to get the effort estimation')
    value = st.text_input(label='KLOC', value='0')
    if value.isdigit():
        on_change(int(value))
    else:
        st.error('Please enter only integer value')
    st.text('Select the mode')
    mode = st.radio(label='Mode', options=['Organic', 'Semi-detached', 'Embedded'])
    st.session_state['MODE'] = mode  # Setting the mode in session state
    st.button(label='Estimate Effort', use_container_width=True, on_click=calculate_effort)
    st.subheader('Cost Estimation')
    st.success(f'Effort = {round(st.session_state["EFFORT"])} PM')
    st.success(f'Month Needed = {round(st.session_state['NUM_OF_MONTHS_NEEDED'])} Months')
    st.success(f'Number of People Needed = {round(st.session_state['NUM_OF_PEOPLE_NEEDED'])} Person')


