document.getElementById('apkForm').addEventListener('submit', function() {
    const btn = document.getElementById('buildBtn');
    const loading = document.getElementById('loading');

    // Show loading state
    btn.disabled = true;
    btn.innerText = 'Compiling...';
    loading.classList.remove('hidden');

    // Re-enable the button after 15 seconds (assuming the download will have started by then)
    setTimeout(() => {
        btn.disabled = false;
        btn.innerText = 'Build & Download APK';
        loading.classList.add('hidden');
    }, 15000); 
});
