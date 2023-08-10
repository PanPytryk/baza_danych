program_status = True


template: dict[str, int | float] = {
    "price": 0,
    "amout": 0
}


account: dict[str, float] = {
    "balance":  10000
    }

warehouse: dict[str, dict[str, int | float]] = {
    "rower": {
            "price": 1399,
            "amout": 6
    },
    "komputer": {
            "price": 5299,
            "amout": 3
    },
    "doniczka": {
            "price": 49,
            "amout": 300
    },
    "lizak": {
            "price": 1,
            "amout": 2000
    },
    "klej_kropela": {
            "price": 7,
            "amout": 1300
    },
    "trampolina": {
            "price": 500,
            "amout": 9
    },
    "siekiera_fiskars": {
            "price": 300,
            "amout": 80
    },
}

history: list[dict[str, str | float | int]] = []


def update_balance(quantum: float):
    record: dict[str, str | float | int] = {
            "type": "accout",
            "balance": account["balance"]
        }

    if account["balance"] + quantum >= 0:
        account["balance"] += quantum

        record["new_balance"] = account["balance"]
        history.append(record)
        return True
    
    
    else:
        print("Brak wystarczających środków na koncie")
        return False


def purchase(product_name: str, price: float, amout: int):
    if update_balance((-1)*amout*price):
        product = warehouse.get(product_name, template.copy())

        product["amout"] += amout
        product["price"] = price
        warehouse[product_name] = product

        history.append(
            {
                "type": "purchase",
                "product_name": product_name,
                "price": product["price"],
                "balance": account["balance"]
            }
        )



def disposal(product_name: str, amout: int):
    product = warehouse.get(product_name)
    if product is not None:
        if amout <= product["amout"]:
            product["amout"] -= amout
            warehouse[product_name] = product
            update_balance(amout*product["price"])

            history.append(
                {
                    "type": "disposal",
                    "product_name": product_name,
                    "price": product["price"],
                    "balance": account["balance"]
                }
            )
    else:
        print("Brak produktu na stanie")


def accout():
    history.append(
        {
            "type": "accout",
            "balance": account["balance"]
        }
    )
    print("Stan konta: ", account.get("balance"))


def get_history(range_l: int, range_r: int) -> list[dict[str, str | float]]:
    return history[range_l:range_r]


def get_overview(start_idx: int, end_idx: int) -> list[dict[str, str | float]]:
    if (start_idx, end_idx) == (0, -1):
        return get_history(start_idx, end_idx)

    history_range = range(len(history))
    if start_idx in history_range and end_idx in history_range:
        if start_idx > end_idx:
            return get_history(end_idx, start_idx)
        else:
            return get_history(start_idx, end_idx)
        
    else:
        return []


def overview(start_idx: int = 0, end_idx: int = -1):
    for record in get_overview(start_idx, end_idx):
        for atr_name, value in record.items():
            print(f"{atr_name}: {value:<10}")
        print()


def warehouse_eq():
    for product_name, value in warehouse.items():
        print(f"{product_name:<10}", end=" ")
        for atr_name, v in value.items():
            print(f"{atr_name}: {v:<10}", end=" ")
        print()


def overview_range(start_idx: int, end_idx: int) -> tuple[int, int]:
    if start_idx == end_idx:
        print("Błędnie podane parametry, zastosowano domyślne")
        return (0, -1)

    elif start_idx < len(history) and end_idx < len(history):
        return (start_idx, end_idx)

    else:
        print("Błędnie podane parametry, zastosowano domyślne")
        return (0, -1)



while program_status is True:
    command = input("Podaj opcję: ").lower()

    if command in ["saldo"]:
        quantum = int(input("quantum: "))
        update_balance(quantum)


    elif command in ["sale", "sprzedaż"]:
        product_name = input("Product name: ")
        amout = int(input("amout: "))
        disposal(product_name, amout)

    elif command in ["purchase", "zakup"]:
        product_name = input("product_name: ")
        price = float(input("price: "))
        amout = int(input("amout: "))

        purchase(product_name, price, amout)
    
    elif command in ["magazyn", "eq"]:
        product_name = input("product name: ")
        on_warehouse = warehouse.get(product_name)
        if on_warehouse is not None:
            print(f"{product_name:<10}", end=" ")
            for atr_name, v in on_warehouse.items():
                print(f"{atr_name}: {v:<10}", end=" ")
            print()
        else:
            print("Brak produktu na stanie")


    elif command in ["lista", "list"]:
        warehouse_eq()

    elif command in ["overview", "przegląd"]:
        start_idx = int(input("start_idx: "))
        end_idx = int(input("end_idx: "))
        overview(*overview_range(start_idx, end_idx)) 




    elif command in ["konto", "balance"]:
        accout()

    elif command == "koniec":
        program_status = False

    else:
        print("Podana komenda nie istnieje")
