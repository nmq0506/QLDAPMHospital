document.addEventListener('DOMContentLoaded', () => {

    const hospitalSelect = document.getElementById('hospital-select');
    const doctorSelect = document.getElementById('doctor-select');
    const dateInput = document.getElementById('appointment-date'); // Lấy element mới
    const timeSlotsContainer = document.getElementById('time-slots-container');


    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);


    function fetchAndDisplaySlots() {
        const doctorId = doctorSelect.value;
        const selectedDate = dateInput.value;


        if (doctorId && selectedDate) {
            timeSlotsContainer.innerHTML = '<p>Loading schedule...</p>';


            fetch(`/get-schedule/${doctorId}?date=${selectedDate}`)
                .then(response => response.json())
                .then(data => {
                    timeSlotsContainer.innerHTML = ''; // Xóa "Loading..."
                    if (data.schedule && data.schedule.length > 0) {
                        data.schedule.forEach((slot, index) => {
                            const slotValue = slot; // "2025-08-15 10:00"
                            const slotTime = new Date(slot).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                            const radio = document.createElement('input');
                            radio.type = 'radio';
                            radio.id = `time-slot-${index}`;
                            radio.name = 'selected_time';
                            radio.value = slotValue;
                            radio.className = 'time-slot-radio';
                            if (index === 0) radio.required = true;

                            const label = document.createElement('label');
                            label.htmlFor = `time-slot-${index}`;
                            label.textContent = slotTime;
                            label.className = 'time-slot-label';

                            timeSlotsContainer.appendChild(radio);
                            timeSlotsContainer.appendChild(label);
                        });
                    } else {
                        timeSlotsContainer.innerHTML = '<p>No available slots for this doctor on the selected date.</p>';
                    }
                })
                .catch(error => console.error('Error fetching schedule:', error));
        }
    }



    hospitalSelect.addEventListener('change', () => {
        const hospitalId = hospitalSelect.value;

        doctorSelect.innerHTML = '<option value="">--Select a location first--</option>';
        doctorSelect.disabled = true;
        dateInput.disabled = true;
        dateInput.value = '';
        timeSlotsContainer.innerHTML = '<p>.</p>';

        if (hospitalId) {
            fetch(`/get-doctors/${hospitalId}`)
                .then(response => response.json())
                .then(data => {
                    doctorSelect.innerHTML = '<option value="">--Chọn bác sĩ--</option>';
                    data.doctors.forEach(doctor => {
                        const option = document.createElement('option');
                        option.value = doctor.id;
                        option.textContent = doctor.name;
                        doctorSelect.appendChild(option);
                    });
                    doctorSelect.disabled = false;
                })
                .catch(error => console.error('Error fetching doctors:', error));
        }
    });


    doctorSelect.addEventListener('change', () => {
        const doctorId = doctorSelect.value;
        timeSlotsContainer.innerHTML = '<p>Chọn bác sĩ và chọn ngày trước.</p>';
        dateInput.value = '';

        if (doctorId) {
            dateInput.disabled = false;
        } else {
            dateInput.disabled = true;
        }
    });


    dateInput.addEventListener('change', fetchAndDisplaySlots);
});