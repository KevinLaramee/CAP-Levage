import QrScanner from './Scanner.min.js';

// function sendResult (label, result) {
      // console.log(label);
      // console.log(result);
// }

function sendResult (result) {
      console.log(result);
}

document.addEventListener('DOMContentLoaded', () => {
  QrScanner.WORKER_PATH = './ScannerWorker.min.js';
  const video = document.getElementById('qr-video');
  const camHasCamera = document.getElementById('cam-has-camera');

  QrScanner.hasCamera().then(hasCamera => camHasCamera.textContent = hasCamera);
  // const scanner = new QrScanner(video, result => sendResult(camQrResult, result));
  const scanner = new QrScanner(video, result => sendResult(result));

  const triggers = document.querySelectorAll('[aria-haspopup="dialog"]');
  const doc = document.querySelector('.js-document');

  const open = function (dialog) {
    dialog.setAttribute('aria-hidden', false);
    doc.setAttribute('aria-hidden', true);

    scanner.start().then(() => {
        scanner.hasFlash().then(hasFlash => {
            // camHasFlash.textContent = hasFlash;
            if (hasFlash) {
                flashToggle.style.display = 'inline-block';
                flashToggle.addEventListener('click', () => {
                    scanner.toggleFlash().then(() => flashState.textContent = scanner.isFlashOn() ? 'on' : 'off');
                });
            }
        });
    });
  };

  const close = function (dialog) {
    dialog.setAttribute('aria-hidden', true);
    doc.setAttribute('aria-hidden', false);

    scanner.stop();
  };

  triggers.forEach((trigger) => {
    const dialog = document.getElementById(trigger.getAttribute('aria-controls'));
    const dismissTriggers = dialog.querySelectorAll('[data-dismiss]');

    // open dialog
    trigger.addEventListener('click', (event) => {
      event.preventDefault();

      open(dialog);
    });

    // close dialog
    dismissTriggers.forEach((dismissTrigger) => {
      const dismissDialog = document.getElementById(dismissTrigger.dataset.dismiss);

      dismissTrigger.addEventListener('click', (event) => {
        event.preventDefault();

        close(dismissDialog);
      });
    });

    window.addEventListener('click', (event) => {
      if (event.target === dialog) {
        close(dialog);
      }
    });
  });
});