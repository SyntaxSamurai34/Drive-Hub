import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Empty list to store user entries
cars = []

@app.route("/")
def home():
    # Build list elements for added cars
    car_list_html = ""
    for car in cars:
        # Determine status badge color dynamically
        badge_style = "background: #2b2b2b; color: #f5f0eb;"  # Default dark
        if car['status'] == 'Available':
            badge_style = "background: #3d5a45; color: #f5f0eb;" # Forest Green accent
        elif car['status'] == 'Not Available':
            badge_style = "background: #8c3b3b; color: #f5f0eb;" # Muted Red accent
        elif car['status'] == 'Gone for Rent':
            badge_style = "background: #b87a2a; color: #f5f0eb;" # Warm Amber accent

        car_list_html += f"""
        <div style="background: #ffffff; border: 1px solid #e0d8ce; padding: 18px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
            <div>
                <h4 style="margin: 0 0 6px 0; color: #1a1a1a; font-size: 18px; font-weight: 600;">{car['brand']} {car['name']}</h4>
                <p style="margin: 0; color: #666058; font-size: 14px;">Colour: <b>{car['colour']}</b></p>
            </div>
            <div>
                <span style="padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; {badge_style}">
                    {car['status']}
                </span>
            </div>
        </div>
        """

    # Message when inventory is empty
    if not cars:
        car_list_html = """
        <div style="text-align: center; padding: 30px; background: #ffffff; border: 1px dashed #d6ccbe; border-radius: 8px; color: #888075;">
            No cars registered yet. Fill out the form above to add your first vehicle.
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Car Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    </head>
    <body style="font-family: 'Inter', Arial, sans-serif; background-color: #f5f0eb; color: #1a1a1a; margin: 0; padding: 40px 20px;">

        <div style="max-width: 650px; margin: 0 auto;">
            
            <!-- Header Header Block -->
            <div style="background-color: #1a1a1a; color: #f5f0eb; padding: 30px; border-radius: 12px 12px 0 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #c2b6a7; font-weight: 600;">PaaS / SaaS Web App</span>
                <h1 style="margin: 8px 0 6px 0; font-size: 26px; font-weight: 700; letter-spacing: -0.5px;">Car Fleet Manager</h1>
                <p style="margin: 0; color: #a39788; font-size: 14px;">Manage vehicle availability and rentals in real time.</p>
            </div>

            <!-- Form Body Container -->
            <div style="background: #fcfaf7; padding: 30px; border-left: 1px solid #e5dccf; border-right: 1px solid #e5dccf; border-bottom: 1px solid #e5dccf; border-radius: 0 0 12px 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.05); margin-bottom: 30px;">
                
                <h3 style="margin-top: 0; margin-bottom: 20px; color: #1a1a1a; font-size: 18px; border-bottom: 2px solid #1a1a1a; padding-bottom: 8px; display: inline-block;">Add New Vehicle</h3>
                
                <form action="/add" method="POST">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                        <div>
                            <label style="font-size: 13px; font-weight: 600; color: #4a453e; display: block; margin-bottom: 6px;">Car Name</label>
                            <input type="text" name="car_name" placeholder="e.g. Civic" required style="width: 100%; padding: 10px 12px; border: 1px solid #d6ccbe; border-radius: 6px; background: #ffffff; box-sizing: border-box; font-family: inherit;">
                        </div>
                        <div>
                            <label style="font-size: 13px; font-weight: 600; color: #4a453e; display: block; margin-bottom: 6px;">Brand</label>
                            <input type="text" name="brand" placeholder="e.g. Honda" required style="width: 100%; padding: 10px 12px; border: 1px solid #d6ccbe; border-radius: 6px; background: #ffffff; box-sizing: border-box; font-family: inherit;">
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                        <div>
                            <label style="font-size: 13px; font-weight: 600; color: #4a453e; display: block; margin-bottom: 6px;">Colour</label>
                            <input type="text" name="colour" placeholder="e.g. Obsidian Black" required style="width: 100%; padding: 10px 12px; border: 1px solid #d6ccbe; border-radius: 6px; background: #ffffff; box-sizing: border-box; font-family: inherit;">
                        </div>
                        <div>
                            <label style="font-size: 13px; font-weight: 600; color: #4a453e; display: block; margin-bottom: 6px;">Availability Status</label>
                            <select name="status" style="width: 100%; padding: 10px 12px; border: 1px solid #d6ccbe; border-radius: 6px; background: #ffffff; box-sizing: border-box; font-family: inherit;">
                                <option value="Available">Available</option>
                                <option value="Not Available">Not Available</option>
                                <option value="Gone for Rent">Gone for Rent</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" style="width: 100%; padding: 12px; background-color: #1a1a1a; color: #f5f0eb; border: none; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: background 0.2s;">
                        Submit Car Entry
                    </button>
                </form>
            </div>

            <!-- Vehicle Inventory List Section -->
            <div style="margin-top: 10px;">
                <h3 style="margin-top: 0; margin-bottom: 15px; color: #1a1a1a; font-size: 18px;">Fleet Inventory</h3>
                {car_list_html}
            </div>

        </div>

    </body>
    </html>
    """

@app.route("/add", methods=["POST"])
def add_car():
    name = request.form.get("car_name")
    brand = request.form.get("brand")
    colour = request.form.get("colour")
    status = request.form.get("status")

    cars.append({
        "name": name,
        "brand": brand,
        "colour": colour,
        "status": status
    })

    return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)