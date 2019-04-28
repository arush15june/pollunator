self.addEventListener('push', (event) => {
   const push_message = event.data.json()
   const title = push_message.title
   console.log(push_message)
   const promiseChain = self.registration.showNotification(title, push_message.       options)

   event.waitUntil(promiseChain)
 })

