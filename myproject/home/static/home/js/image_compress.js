(function () {
    var MAX_BYTES = 3.5 * 1024 * 1024; // 3.5 MB — safe headroom under Vercel's 4.5 MB cap
    var MAX_DIM   = 2400;               // max pixel dimension after resize

    function compress(file, done) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = new Image();
            img.onload = function () {
                var w = img.width, h = img.height;
                if (w > MAX_DIM || h > MAX_DIM) {
                    if (w >= h) { h = Math.round(h * MAX_DIM / w); w = MAX_DIM; }
                    else        { w = Math.round(w * MAX_DIM / h); h = MAX_DIM; }
                }
                var canvas = document.createElement('canvas');
                canvas.width = w; canvas.height = h;
                canvas.getContext('2d').drawImage(img, 0, 0, w, h);

                var quality = 0.88;
                (function attempt() {
                    canvas.toBlob(function (blob) {
                        if (blob.size <= MAX_BYTES || quality <= 0.25) {
                            done(new File([blob], file.name.replace(/\.[^.]+$/, '.jpg'), {
                                type: 'image/jpeg', lastModified: Date.now()
                            }));
                        } else {
                            quality = Math.round((quality - 0.1) * 100) / 100;
                            attempt();
                        }
                    }, 'image/jpeg', quality);
                })();
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    function attach(input) {
        if (input._imgCompress) return;
        input._imgCompress = true;
        input.addEventListener('change', function () {
            var file = this.files[0];
            if (!file || !file.type.startsWith('image/') || file.size <= MAX_BYTES) return;
            var self = this;
            var note = document.createElement('small');
            note.textContent = ' Compressing…';
            note.style.cssText = 'color:#666;margin-left:8px;';
            if (self.parentNode) self.parentNode.appendChild(note);
            compress(file, function (compressed) {
                try {
                    var dt = new DataTransfer();
                    dt.items.add(compressed);
                    self.files = dt.files;
                } catch (_) {}
                note.remove();
            });
        });
    }

    function scan() {
        document.querySelectorAll('input[type="file"]').forEach(attach);
    }

    document.addEventListener('DOMContentLoaded', scan);

    // Catch Wagtail modal/chooser inputs added after page load
    new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
            m.addedNodes.forEach(function (node) {
                if (node.nodeType !== 1) return;
                if (node.matches('input[type="file"]')) attach(node);
                node.querySelectorAll('input[type="file"]').forEach(attach);
            });
        });
    }).observe(document.documentElement, { childList: true, subtree: true });
})();
