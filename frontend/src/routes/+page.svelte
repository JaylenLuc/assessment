<script> 
    import { Button } from '../lib/components/ui/button';
    import { Input } from '../lib/components/ui/input';
    import { Label } from '../lib/components/ui/label';
    import axios from 'axios';
    let orderRequest = "";
    let responseMessage = "";
    /**
     * @type {any[]}
     */
    let orders = []
    let totals = {"burgers" : 0, "fries" : 0, "drinks": 0}
    let showAlert = false;
    let alertMessage = "";
    let alertType = "";  // "success" or "error"
    
    async function addOrder(){
        
        try{
            const data = { text: orderRequest };
            // const res = await fetch('https://solid-halibut-v75479p7j9q2x4qr-8000.app.github.dev/askchat', {
            //     method: 'POST',
            //     headers: 
            //         {
            //             'Content-Type': 'application/json',
                        
            //         },
            //     body: JSON.stringify(data),
            //     credentials: 'include' 
            // })
            console.log("Attempting to send order:", orderRequest);
    
            const API_URL =  import.meta.env.VITE_API_URL;
        
        // First, try a preflight request
            
            const res = await axios({
                method: 'post',
                url: API_URL,
                data: data,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                withCredentials: false,
            });

        console.log("Response:", res.data);
            if (res.data && res.data.message) {
                console.log("OK")
                const responseMessage = await res.data.message; // Parse the JSON response
                // responseMessage = data.message; // Extract the message from the response
                //quant item, quant item, ....
                //cancel order num
                const hasCancel = responseMessage.toLowerCase().includes("cancel");
                const hasInvalid = responseMessage.toLowerCase().includes("invalid");

                //CASES CAN EXTEND WITH ANOTHER ELSE IF BEFORE THE ELSE CASE
                if (hasCancel){
                    let cancelMessage = responseMessage.split(' ')[2];
                    const index = Number(cancelMessage) - 1
                    console.log(index)
                    let currOrder = orders[index]
                    if (currOrder == undefined){
                        //ALERT CASES
                        alertType = "error";
                        alertMessage = `Your request to cancel order ${index +1} is invalid`
                        showAlert = true;
                        setTimeout(() => showAlert = false, 2000); // Hide after 2 seconds
                        return;

                    }
                    totals["burgers"] -= currOrder["burgers"]
                    totals["fries"] -= currOrder["fries"]
                    totals["drinks"] -=  currOrder["drinks"]
                    orders = orders.filter((_, i) => i !== index);


                    alertType = "success";
                    alertMessage = `Your request to cancel order number ${index+1} has been successfull!!`
                    showAlert = true;
                    setTimeout(() => showAlert = false, 2000); // Hide after 2 seconds
                }else if (hasInvalid){
                    //invalid entry deal with it
                    alertType = "error";
                    alertMessage = "Your request was invalid :( "
                    showAlert = true;
                    setTimeout(() => showAlert = false, 2000); // Hide after 2 seconds
                }
                else{ //VALID ORDER CASE
                    let orderObject = {"burgers" : 0, "fries" : 0, "drinks": 0}
                    let responseArray = responseMessage.split(', ').forEach((/** @type {string} */ itemarr) => {
                        let singleOrder = itemarr.split(' ');
                        let quant = Number(singleOrder[0])
                        let item = singleOrder[1]
                        
                        
                        const hasBurger = item.toLowerCase().includes("burger") || item.toLowerCase().includes("burgers")
                        const hasFries = item.toLowerCase().includes("fries") || item.toLowerCase().includes("fry")
                        const hasDrinks = item.toLowerCase().includes("drink") || item.toLowerCase().includes("drinks")
                        if (hasBurger){
                            orderObject["burgers"] +=  quant
                        }                        
                        else if (hasFries){
                            orderObject["fries"] +=  quant
                        }
                        else if (hasDrinks){
                            orderObject["drinks"] +=  quant
                        }

                    });
                    orders = [...orders, orderObject];
                    //orders.push(orderObject)
                    console.log("all orders: ", orders)
                    totals["burgers"] +=  orderObject["burgers"]
                    totals["fries"] +=  orderObject["fries"]
                    totals["drinks"] +=  orderObject["drinks"]
                    console.log(totals)
                    alertType = "success";
                    alertMessage = "Your Order has been placed successfully!"
                    showAlert = true;
                    setTimeout(() => showAlert = false, 2000); // Hide after 2 seconds
                    
                }


            } else {

                console.log(`Error: ${res.status} ${res.statusText}`);
            }
        }catch(error){
            // @ts-ignore
            console.log(`Error: ${error.message}`);
        }
        orderRequest = "";
    }

</script>

<main>
    <div class="flex items-center justify-center h-64 bg-gray-200">
        
        <div class="w-1/5 p-6 bg-gray-100 rounded-lg">
            <Label>Total amount of items ordered</Label>
            <Input disabled value={`${totals.burgers} burgers ordered`}/> 
            <Input disabled value={`${totals.fries} fries ordered`}/> 
            <Input disabled value={`${totals.drinks} drinks ordered`}/> 
        </div>
    </div>
    <div class="flex items-center justify-center h-64 bg-gray-200">
        <div class="w-1/2 p-6 bg-gray-100 rounded-lg">
            <Label>Enter your order</Label>
            <Input 
                bind:value={orderRequest}  
                placeholder="enter your order request"/> 
        </div>
        <Button 
            disabled={!orderRequest.trim()} 
            class="w-[80px] h-[80px]"
            on:click={addOrder}
        >
            Run
        </Button>
    </div>
        <!-- Display Orders -->
    <div class="mt-6 p-6 bg-gray-100 rounded-lg">
    <Label>Orders</Label>
    <ul>
        {#each orders as order, index (order)}
        <li class="p-2 border-b-2">
            Order #{index + 1}: 
            {order.burgers} burgers, 
            {order.fries} fries, 
            {order.drinks} drinks
        </li>
        {/each}
    </ul>
    </div>
      <!-- Alert Message -->
    {#if showAlert}
    <div class={`fixed top-0 left-0 right-0 p-4 ${alertType === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white text-center`}>
        {alertMessage}
    </div>
    {/if}
</main>

<style>
    ul {
      list-style-type: none;
      padding: 0;
    }
  
    li {
      padding: 10px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 8px;
      background-color: #f9f9f9;
    }
  
    .order-item {
      font-size: 16px;
      color: #333;
    }
  </style>
