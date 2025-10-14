// TodoアプリのJavaScript機能

document.addEventListener('DOMContentLoaded', function () {
    // フォームのバリデーション
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const titleInput = form.querySelector('input[name="title"]');
            if (titleInput && !titleInput.value.trim()) {
                e.preventDefault();
                showAlert('タイトルは必須です', 'error');
                titleInput.focus();
            }
        });
    });

    // 自動でアラートを非表示にする
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // チェックボックスのアニメーション
    const checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const card = this.closest('.card');
            if (this.checked) {
                card.classList.add('border-success');
                card.classList.remove('border-warning');
            } else {
                card.classList.add('border-warning');
                card.classList.remove('border-success');
            }
        });
    });

    // 文字数カウント（説明欄）
    const descriptionTextarea = document.getElementById('description');
    if (descriptionTextarea) {
        const maxLength = 500;
        const counter = document.createElement('small');
        counter.className = 'text-muted';
        counter.style.float = 'right';
        descriptionTextarea.parentNode.appendChild(counter);

        function updateCounter() {
            const remaining = maxLength - descriptionTextarea.value.length;
            counter.textContent = `${descriptionTextarea.value.length}/${maxLength}`;
            if (remaining < 0) {
                counter.className = 'text-danger';
            } else if (remaining < 50) {
                counter.className = 'text-warning';
            } else {
                counter.className = 'text-muted';
            }
        }

        descriptionTextarea.addEventListener('input', updateCounter);
        updateCounter();
    }
});

// アラート表示関数
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);

    // 5秒後に自動で非表示
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// Todoの完了状態を切り替える関数
function toggleTodo(todoId) {
    // ローディング表示
    const checkbox = event.target;
    const originalState = checkbox.checked;
    checkbox.disabled = true;

    // リクエストを送信
    fetch(`/toggle/${todoId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => {
            if (response.ok) {
                // 成功時はページをリロード
                window.location.reload();
            } else {
                // エラー時はチェックボックスを元に戻す
                checkbox.checked = !originalState;
                checkbox.disabled = false;
                showAlert('エラーが発生しました', 'error');
            }
        })
        .catch(error => {
            // エラー時はチェックボックスを元に戻す
            checkbox.checked = !originalState;
            checkbox.disabled = false;
            showAlert('ネットワークエラーが発生しました', 'error');
        });
}

// 削除確認の強化
function confirmDelete(todoTitle) {
    return confirm(`「${todoTitle}」を削除しますか？\nこの操作は取り消せません。`);
}

// キーボードショートカット
document.addEventListener('keydown', function (e) {
    // Ctrl+Enter でフォーム送信
    if (e.ctrlKey && e.key === 'Enter') {
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    }

    // Escape でモーダルを閉じる
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// ダークモード切り替え（オプション機能）
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// ページ読み込み時にダークモード設定を復元
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}
