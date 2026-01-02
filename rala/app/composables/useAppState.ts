import { ref } from 'vue'

// Global app state
const isLoading = ref(true)

export const useAppState = () => {
  const setLoading = (value: boolean) => {
    isLoading.value = value
  }

  return {
    isLoading,
    setLoading
  }
}
