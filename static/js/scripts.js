document.addEventListener('DOMContentLoaded', function() {
    // Функция для отправки формы и обработки результата
    function submitForm(formId, resultDivId) {
        const form = document.getElementById(formId);
        const resultDiv = document.getElementById(resultDivId);
        const preloader = document.getElementById('preloader');
        
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Останавливаем стандартную отправку формы

            const formData = new FormData(form);
            const url = form.action || window.location.href;

            // Показываем индикатор загрузки
            preloader.style.display = 'block';
            resultDiv.innerHTML = ''; // Очищаем предыдущее содержимое

            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // Скрываем индикатор загрузки
                preloader.style.display = 'none';

                // Показываем результат
                if (data.success) {
                    resultDiv.innerHTML = '<pre>' + JSON.stringify(data.result, null, 4) + '</pre>';
                } else {
                    resultDiv.innerHTML = '<p>Error: ' + data.error + '</p>';
                }
            })
            .catch(error => {
                // В случае ошибки скрываем загрузку и выводим ошибку
                preloader.style.display = 'none';
                resultDiv.innerHTML = '<p>Something went wrong: ' + error.message + '</p>';
            });
        });
    }

    // Привязываем обработчики для каждой формы
    submitForm('scan_ports_form', 'scan_ports_result');
    submitForm('lookup_ip_form', 'lookup_ip_result');
    submitForm('ping_form', 'ping_result');
    submitForm('traceroute_form', 'traceroute_result');
    submitForm('geoip_form', 'geoip_result');
    submitForm('dns_lookup_form', 'dns_lookup_result');
    submitForm('reverse_dns_form', 'reverse_dns_result');
});
