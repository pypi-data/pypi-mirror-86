import r from"./useDebounce.js";const t=e=>Array.isArray(e)&&!e.length||typeof e=="string"&&e==="",s=(e,n=275)=>{const i=r(e,n);return t(e)||t(i)?e:i};export default s;
