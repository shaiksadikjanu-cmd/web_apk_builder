// 1. We wrap your original building logic inside a global function.
// The Android Java code will call this specific function when the video ad finishes!
function startApkBuild() {
    const btn = document.getElementById('buildBtn');
    const loading = document.getElementById('loading');
    const form = document.getElementById('apkForm');

    // Show your beautiful loading state
    btn.disabled = true;
    btn.innerText = 'Compiling...';
    loading.classList.remove('hidden');

    // FORCE the form to submit to your Python backend now that the ad is done
    form.submit();

    // Re-enable the button after 15 seconds just like you designed
    setTimeout(() => {
        btn.disabled = false;
        btn.innerText = 'Build & Download APK';
        loading.classList.add('hidden');
    }, 15000); 
}

// 2. We hijack the button click to check for the AdMob Bridge first
document.getElementById('apkForm').addEventListener('submit', function(event) {
    // STOP the form from submitting instantly! 
    event.preventDefault(); 
    
    const btn = document.getElementById('buildBtn');
    
    // THE BRIDGE CHECK: Is the user inside your Android App?
    if (typeof window.AndroidApp !== "undefined") {
        
        // Change the button text so the user knows an ad is loading
        btn.innerText = '📺 Loading Reward Video...';
        btn.disabled = true;
        
        // Trigger the Java code to play the AdMob video!
        window.AndroidApp.requestAd();
        
    } else {
        // If they are on a laptop browser, just build it normally without ads
        startApkBuild();
    }
});
