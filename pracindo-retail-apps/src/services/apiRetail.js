import api from './api' 
const R = 'retail' 

export const apiCabang = {
  buat: (data) => api.post(`${R}/cabang/`, data).then((r) => r.data),
}