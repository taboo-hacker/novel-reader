/*
 * 小说阅读器前端脚本
 * 实现交互功能，如深色模式切换、字体大小调整、书签添加等
 */

// 页面加载完成后执行
window.addEventListener('DOMContentLoaded', function() {
    // 初始化页面状态
    initPage();
    
    // 绑定事件监听器
    bindEventListeners();
});

/**
 * 初始化页面状态
 * 从本地存储中恢复用户设置
 */
function initPage() {
    // 恢复深色模式设置
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
    
    // 恢复字体大小设置
    const fontSize = localStorage.getItem('fontSize') || 'medium';
    setFontSize(fontSize);
    
    // 恢复书签提示
    const bookmark = localStorage.getItem('bookmark');
    if (bookmark) {
        try {
            const bookmarkData = JSON.parse(bookmark);
            showBookmarkNotification(bookmarkData);
        } catch (e) {
            console.error('解析书签数据失败:', e);
        }
    }
}

/**
 * 绑定事件监听器
 */
function bindEventListeners() {
    // 深色模式切换
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', toggleDarkMode);
    }
    
    // 字体大小调整
    const fontDecrease = document.getElementById('font-decrease');
    const fontIncrease = document.getElementById('font-increase');
    
    if (fontDecrease) {
        fontDecrease.addEventListener('click', decreaseFontSize);
    }
    
    if (fontIncrease) {
        fontIncrease.addEventListener('click', increaseFontSize);
    }
    
    // 添加书签
    const addBookmark = document.getElementById('add-bookmark');
    if (addBookmark) {
        addBookmark.addEventListener('click', addBookmarkHandler);
    }
}

/**
 * 切换深色模式
 */
function toggleDarkMode() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
    
    // 更新按钮文本
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.textContent = isDarkMode ? '浅色模式' : '深色模式';
    }
}

/**
 * 减小字体大小
 */
function decreaseFontSize() {
    const currentSize = localStorage.getItem('fontSize') || 'medium';
    const sizes = ['small', 'medium', 'large', 'xlarge'];
    const currentIndex = sizes.indexOf(currentSize);
    
    if (currentIndex > 0) {
        const newSize = sizes[currentIndex - 1];
        setFontSize(newSize);
        localStorage.setItem('fontSize', newSize);
    }
}

/**
 * 增大字体大小
 */
function increaseFontSize() {
    const currentSize = localStorage.getItem('fontSize') || 'medium';
    const sizes = ['small', 'medium', 'large', 'xlarge'];
    const currentIndex = sizes.indexOf(currentSize);
    
    if (currentIndex < sizes.length - 1) {
        const newSize = sizes[currentIndex + 1];
        setFontSize(newSize);
        localStorage.setItem('fontSize', newSize);
    }
}

/**
 * 设置字体大小
 * @param {string} size - 字体大小，可选值：small, medium, large, xlarge
 */
function setFontSize(size) {
    const contentElement = document.querySelector('.chapter-content .content');
    if (contentElement) {
        // 移除所有字体大小类
        contentElement.classList.remove('font-size-small', 'font-size-medium', 'font-size-large', 'font-size-xlarge');
        
        // 添加新的字体大小类
        contentElement.classList.add(`font-size-${size}`);
    }
}

/**
 * 添加书签
 */
function addBookmarkHandler() {
    const chapterTitle = document.querySelector('h2')?.textContent;
    const currentUrl = window.location.href;
    
    if (chapterTitle) {
        const bookmarkData = {
            title: chapterTitle,
            url: currentUrl,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('bookmark', JSON.stringify(bookmarkData));
        showNotification('书签已添加', 'success');
    } else {
        showNotification('当前页面无法添加书签', 'error');
    }
}

/**
 * 显示书签通知
 * @param {Object} bookmarkData - 书签数据
 */
function showBookmarkNotification(bookmarkData) {
    if (bookmarkData && bookmarkData.url !== window.location.href) {
        const notification = document.createElement('div');
        notification.className = 'bookmark-notification';
        notification.innerHTML = `
            <p>上次阅读: <a href="${bookmarkData.url}">${bookmarkData.title}</a></p>
            <button id="dismiss-bookmark">关闭</button>
        `;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
        `;
        
        document.body.appendChild(notification);
        
        // 绑定关闭按钮事件
        document.getElementById('dismiss-bookmark').addEventListener('click', function() {
            notification.remove();
        });
        
        // 3秒后自动关闭
        setTimeout(function() {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

/**
 * 显示通知
 * @param {string} message - 通知消息
 * @param {string} type - 通知类型，可选值：success, error, info
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // 设置通知样式
    const bgColor = {
        success: '#4CAF50',
        error: '#f44336',
        info: '#2196F3'
    }[type] || '#2196F3';
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: ${bgColor};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    // 添加动画
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // 3秒后自动关闭
    setTimeout(function() {
        if (notification.parentNode) {
            notification.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(function() {
                notification.remove();
                style.remove();
            }, 300);
        }
    }, 3000);
}

/**
 * 平滑滚动到指定元素
 * @param {HTMLElement} element - 目标元素
 */
function smoothScrollTo(element) {
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * 检测移动设备
 * @returns {boolean} 是否为移动设备
 */
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * 处理移动设备的特殊交互
 */
function handleMobileInteraction() {
    if (isMobileDevice()) {
        // 为移动设备添加特殊处理
        console.log('检测到移动设备');
        
        // 例如：调整触摸目标大小
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.style.minHeight = '44px';
            button.style.minWidth = '44px';
        });
    }
}

// 处理移动设备交互
handleMobileInteraction();
