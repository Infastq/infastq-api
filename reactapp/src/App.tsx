import Navbar from "./components/Navbar"
import { getSummary } from "./services/summary.service"
import { useEffect, useState } from "react"

function App() {

  const [summary, setSummary] = useState(1)
  
  console.log(getSummary());

  // useEffect(() => {
  //   getSummary().then((res) => {
  //     setSummary(res.data.total_uang)
  //   }).catch((err) => {
  //     console.log(err)
  //   })
  // },[summary])

  return (
    <div className="bg-[rgba(0,0,0,0.2)] bg-cover w-screen h-screen">
      <div className="">
        <Navbar />
      </div>
      <div className="flex flex-col justify-center items-center">
        <h1 className="font-bold text-cente my-16 text-4xl">Kotak Amal 1</h1>
        <div className="w-[400px] h-[400px] rounded-full bg-transparent border-[10px] border-[#04387D]  text-center relative">
          <h3 className="flex justify-center items-center font-bold text-4xl text-[#04387D] absolute inset-0">{formatPrice(summary)}</h3>
        </div>
      </div>
    </div>
  )
}

const formatPrice = (price : number) => {
  return price.toLocaleString("id-ID", {
    style: "currency",
    currency: "IDR",
  })
};

export default App
