import React, { useEffect, useState } from 'react'

const SubscriptionDisplay = () => {
  const [subscription, setSubscription] = useState(null)

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/last-subscription`)
        const data = await res.json()
        if (data.username) setSubscription(data)
      } catch (err) {
        console.error("Error al obtener suscripción:", err)
      }
    }

    fetchSubscription()
    const interval = setInterval(fetchSubscription, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <h2>📡 Última suscripción</h2>
      {subscription ? (
        <ul>
          <li><strong>Usuario:</strong> {subscription.username}</li>
          <li><strong>Cuota mensual:</strong> ${subscription.monthly_fee}</li>
          <li><strong>Fecha de inicio:</strong> {new Date(subscription.start_date).toLocaleString()}</li>
        </ul>
      ) : (
        <p>Esperando datos…</p>
      )}
    </div>
  )
}

export default SubscriptionDisplay