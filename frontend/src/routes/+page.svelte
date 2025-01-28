<script> 
    import { Button } from '../lib/components/ui/button';
    import { Input } from '../lib/components/ui/input';
    import { Label } from '../lib/components/ui/label';
    let orderRequest = "";
    let responseMessage = "";
    let orders = []
    let totals = {"burgers" : 0, "fries" : 0, "drinks": 0}
    async function addOrder(){
        console.log("here11111")
        
        try{
            const data = { text: orderRequest };
            const res = await fetch('http://127.0.0.1:8000/askchat', {
                method: 'POST',
                headers: 
                    {
                        'Content-Type': 'application/json'
                    },
                body: JSON.stringify(data)
            })
            if (res.ok) {
                console.log("OK")
                const data = await res.json(); // Parse the JSON response
                responseMessage = data.message; // Extract the message from the response
                //quant item, quant item, ....
                //cancel order num
                const hasCancel = responseMessage.toLowerCase().includes("cancel");
                const hasInvalid = responseMessage.toLowerCase().includes("invalid");
                if (hasCancel){
                    //TO DO 
                }else if (hasInvalid){
                    //invalid entry deal with it
                }
                else{
                    let orderObject = {"burgers" : 0, "fries" : 0, "drinks": 0}
                    let responseArray = responseMessage.split(', ').forEach(itemarr => {
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

                    orders.push(orderObject)
                    totals["burgers"] +=  orderObject["burgers"]
                    totals["fries"] +=  orderObject["fries"]
                    totals["drinks"] +=  orderObject["drinks"]
                    console.log(totals)
                    
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
</main>
