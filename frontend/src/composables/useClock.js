import { ref, onMounted, onUnmounted } from 'vue'

const weekMap = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']

export function useClock() {
  const clockTime = ref('')
  const clockDate = ref('')
  const clockWeek = ref('')
  let clockTimer = null

  const pad = (n) => String(n).padStart(2, '0')

  const updateClock = () => {
    const now = new Date()
    clockTime.value = `${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`
    clockDate.value = `${now.getFullYear()}.${pad(now.getMonth() + 1)}.${pad(now.getDate())}`
    clockWeek.value = weekMap[now.getDay()]
  }

  onMounted(() => {
    updateClock()
    clockTimer = setInterval(updateClock, 1000)
  })

  onUnmounted(() => {
    if (clockTimer) clearInterval(clockTimer)
  })

  return {
    clockTime,
    clockDate,
    clockWeek,
  }
}
