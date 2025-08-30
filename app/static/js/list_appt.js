document.addEventListener('DOMContentLoaded', function() {

            // Hàm hiển thị hộp thoại xác nhận bằng SweetAlert2
            function showConfirmDialog(title, text, onConfirm) {
                Swal.fire({
                    title: title,
                    text: text,
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#0d6efd',
                    cancelButtonColor: '#6c757d',
                    confirmButtonText: 'Xác nhận',
                    cancelButtonText: 'Hủy bỏ'
                }).then((result) => {

                    if (result.isConfirmed) {
                        onConfirm();
                    }
                });
            }


            function handleApiCall(button, url) {

                const card = button.closest('.appointment-card');
                fetch(url)
                    .then(response => {
                        if (response.ok) {
                            location.reload();

                            Swal.fire(
                                'Thành công!'
                            );

                        } else {
                            Swal.fire(
                                'Lỗi!',
                                'Đã có lỗi xảy ra. Vui lòng thử lại.',
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Lỗi!',
                            'Không thể kết nối đến máy chủ.',
                            'error'
                        );
                    });
            }


            document.querySelectorAll('.btn-cancel').forEach(button => {
                button.addEventListener('click', function() {
                    const apptId = this.dataset.id;
                    const url = `/change-status/${apptId}`;
                    showConfirmDialog(
                        'Xác nhận hủy lịch',
                        'Bạn có chắc chắn muốn hủy lịch hẹn này không?',
                        () => handleApiCall(this, url)
                    );
                });
            });


            document.querySelectorAll('.btn-complete').forEach(button => {
                button.addEventListener('click', function() {
                    const apptId = this.dataset.id;
                    const url = `/complete-appointment/${apptId}`;
                    showConfirmDialog(
                        'Xác nhận hoàn thành',
                        'Bạn có muốn đánh dấu lịch hẹn này là đã hoàn thành không?',
                        () => handleApiCall(this, url)
                    );
                });
            });

        });

