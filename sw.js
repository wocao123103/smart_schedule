/* 智能日程助手 · Service Worker
 * 只负责系统通知与点击回到页面，不做缓存，避免 GitHub Pages 更新后看到旧版本。
 */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => event.waitUntil(self.clients.claim()));

/* 空 fetch 监听让浏览器把本站识别为可安装 PWA；不缓存，避免更新滞后。 */
self.addEventListener('fetch', () => {});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((list) => {
      for (const client of list) {
        if ('focus' in client) return client.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow('./');
    })
  );
});
