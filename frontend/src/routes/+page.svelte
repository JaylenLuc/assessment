<script> 
    import {Button} from '../lib/components/ui/button';
    import { Input } from '../lib/components/ui/input';
    import { Label } from '../lib/components/ui/label';
    let orderRequest = "";
</script>

<main>
    <div class="flex items-center justify-center h-64 bg-gray-200">
        
        <div class="w-1/5 p-6 bg-gray-100 rounded-lg">
            <Label>Total amount of items ordered</Label>
            <Input disabled value=" burgers ordered"/> 
            <Input disabled value=" fries ordered"/> 
            <Input disabled value=" drinks ordered"/> 
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
        >
            Run
        </Button>
    </div>
</main>
