(function () {
    var SIGN_URL = '/admin-api/cloudinary-sign-upload/';
    var MAX_BYTES = 9.5 * 1024 * 1024; // keep in sync with CLOUDINARY_DIRECT_UPLOAD_MAX_BYTES

    // Inject once: make the in-progress state impossible to miss (a quietly
    // disabled submit button reads as "the modal froze" otherwise).
    var style = document.createElement('style');
    style.textContent =
        '.cloudinary-direct-status { display: inline-block; margin-top: 6px; font-weight: 600; font-size: 13px; }' +
        '.cloudinary-direct-status--busy { color: #1a56db; }' +
        '.cloudinary-direct-status--error { color: #c0392b; }' +
        '.cloudinary-direct-status--ok { color: #1a7f37; }' +
        'button[data-cloudinary-busy]:disabled { opacity: 0.6; cursor: wait; }';
    document.head.appendChild(style);

    function statusFor(input) {
        return document.querySelector('.cloudinary-direct-status[data-status-for="' + input.dataset.target + '"]');
    }

    function setStatus(input, message, kind) {
        var status = statusFor(input);
        if (!status) return;
        status.textContent = message || '';
        status.className = 'cloudinary-direct-status' + (kind ? ' cloudinary-direct-status--' + kind : '');
    }

    function toggleSubmit(form, disabled) {
        if (!form) return;
        form.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(function (btn) {
            btn.disabled = disabled;
            btn.toggleAttribute('data-cloudinary-busy', disabled);
            if (btn.tagName === 'BUTTON') {
                var label = btn.querySelector('em') || btn;
                if (disabled) {
                    if (btn.dataset.cloudinaryOrigLabel === undefined) {
                        btn.dataset.cloudinaryOrigLabel = label.textContent;
                    }
                    label.textContent = 'Waiting for image upload…';
                } else if (btn.dataset.cloudinaryOrigLabel !== undefined) {
                    label.textContent = btn.dataset.cloudinaryOrigLabel;
                    delete btn.dataset.cloudinaryOrigLabel;
                }
            }
        });
    }

    function handleFile(input, file) {
        if (!file) return;
        if (!file.type.startsWith('image/')) {
            setStatus(input, 'Please choose an image file.', 'error');
            input.value = '';
            return;
        }
        if (file.size > MAX_BYTES) {
            setStatus(input, 'That file is ' + (file.size / 1024 / 1024).toFixed(1) + 'MB — please choose one under ' + (MAX_BYTES / 1024 / 1024).toFixed(1) + 'MB.', 'error');
            input.value = '';
            return;
        }

        var form = input.closest('form');
        var hidden = document.getElementById(input.dataset.target);
        toggleSubmit(form, true);
        setStatus(input, 'Uploading image, please wait…', 'busy');

        fetch(SIGN_URL, { credentials: 'same-origin' })
            .then(function (r) {
                if (!r.ok) throw new Error('Could not start upload (are you signed in?)');
                return r.json();
            })
            .then(function (sign) {
                var body = new FormData();
                body.append('file', file);
                body.append('api_key', sign.api_key);
                body.append('timestamp', sign.timestamp);
                body.append('signature', sign.signature);
                body.append('folder', sign.folder);
                body.append('use_filename', sign.use_filename);
                body.append('unique_filename', sign.unique_filename);

                return fetch('https://api.cloudinary.com/v1_1/' + sign.cloud_name + '/image/upload', {
                    method: 'POST',
                    body: body,
                }).then(function (r) {
                    if (!r.ok) throw new Error('Cloudinary rejected the upload.');
                    return r.json();
                });
            })
            .then(function (result) {
                if (!result.public_id) throw new Error('Upload succeeded but no file was returned.');
                if (hidden) {
                    hidden.value = result.public_id;
                    hidden.dispatchEvent(new Event('input', { bubbles: true }));
                    hidden.dispatchEvent(new Event('change', { bubbles: true }));
                }
                setStatus(input, 'Image uploaded — you can click Upload now.', 'ok');
            })
            .catch(function (err) {
                setStatus(input, err.message || 'Upload failed — please try again.', 'error');
            })
            .finally(function () {
                toggleSubmit(form, false);
            });
    }

    function attach(input) {
        if (input._cloudinaryDirect) return;
        input._cloudinaryDirect = true;
        input.addEventListener('change', function () {
            handleFile(input, input.files[0]);
        });
    }

    function scan() {
        document.querySelectorAll('input[data-cloudinary-direct]').forEach(attach);
    }

    document.addEventListener('DOMContentLoaded', scan);

    // Catch Wagtail modal/chooser inputs added after page load
    new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
            m.addedNodes.forEach(function (node) {
                if (node.nodeType !== 1) return;
                if (node.matches && node.matches('input[data-cloudinary-direct]')) attach(node);
                if (node.querySelectorAll) node.querySelectorAll('input[data-cloudinary-direct]').forEach(attach);
            });
        });
    }).observe(document.documentElement, { childList: true, subtree: true });
})();
