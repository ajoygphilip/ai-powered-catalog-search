<script>
  // @ts-nocheck

  import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
  import { Card, Button, Rating, Badge } from 'flowbite-svelte';
  import { PaginationNav, Pagination, PaginationItem } from 'flowbite-svelte';
  import { Label, Input } from 'flowbite-svelte';

  let data = $state(null);

  async function load(url) {
    const res = await fetch(url);
    console.log(data?.res);
    data = await res.json();
  }

  let url = $state('http://localhost:8000/catalog/products/');
  load(url);
</script>

<div class="p-0 m-0 box-border flex flex-col">
  <Navbar>
    <NavBrand href="/">
      <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">Flowbite</span>
    </NavBrand>
    <NavHamburger />
    <NavUl>
      <NavLi href="/">Home</NavLi>
      <NavLi href="/about">About</NavLi>
      <NavLi href="/docs/components/navbar">Navbar</NavLi>
      <NavLi href="/pricing">Pricing</NavLi>
      <NavLi href="/contact">Contact</NavLi>
    </NavUl>
  </Navbar>
  <div class="mb-6 p-8">
    <Input
      id="large-input"
      size="md"
      placeholder="search for products"
      onkeydown={e => e.key == 'Enter' && load(`http://localhost:8000/catalog/products?search=${e.target.value}`)}
    />
  </div>
  <div class="flex flex-row flex-wrap gap-4 justify-center items-center">
    {#each data?.results as product}
      <Card class="m-4 max-w-[300px]">
        <a href="#">
          <img class="rounded-t-sm p-6" src={product.image} alt="product 1" />
        </a>
        <div class="px-5 pb-5">
          <a href="/">
            <h5 class="text-xl font-semibold tracking-tight text-gray-900 dark:text-white">{product.name}</h5>
          </a>

          <div class="flex items-center justify-between">
            <span class="text-2xl font-bold text-gray-900 dark:text-white">${product.price}</span>
            <Button href="/">Buy now</Button>
          </div>
        </div>
      </Card>
    {/each}
  </div>
</div>
<div class="flex space-x-3 rtl:space-x-reverse">
  <PaginationItem size="large" onclick={() => data?.previous && load(data.previous)}>Previous</PaginationItem>
  <PaginationItem size="large" onclick={() => data?.next && load(data.next)}>Next</PaginationItem>
</div>
