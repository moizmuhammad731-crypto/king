"""Generate the reference-style diagrams for the NED-format Pink Wheels report."""

import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, FancyArrowPatch

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

BLUE_FC, BLUE_EC = "#E8F1F9", "#8FB3D9"
TAN_FC, TAN_EC = "#F8F1E3", "#C4A97A"
GREY_FC, GREY_EC = "#F2F2F2", "#9A9A9A"
TEXT = "#1A1A1A"


def canvas(w, h, xmax, ymax):
    fig = plt.figure(figsize=(w, h), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=BLUE_FC, ec=BLUE_EC, fs=7.4, rounded=0.8, bold=False):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.25,rounding_size={rounded}",
        linewidth=0.9, edgecolor=ec, facecolor=fc,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=TEXT, linespacing=1.35,
            fontweight="bold" if bold else "normal")


def rect(ax, x, y, w, h, text, fc=GREY_FC, ec=GREY_EC, fs=7.4, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, linewidth=0.9, edgecolor=ec, facecolor=fc))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, color=TEXT, linespacing=1.3,
            fontweight="bold" if bold else "normal")


def diamond(ax, cx, cy, w, h, text, fc=GREY_FC, ec=GREY_EC, fs=7.0):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(plt.Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, linewidth=0.9))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=TEXT, linespacing=1.25)


def arrow(ax, p1, p2, label=None, fs=6.1, rad=0.0, lx=0, ly=0):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle="-|>", mutation_scale=7.5,
        linewidth=0.8, color="#5A5A5A",
        connectionstyle=f"arc3,rad={rad}",
    ))
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color="#333333", bbox=dict(fc="white", ec="none", pad=0.7))


def poly_arrow(ax, pts, label=None, fs=6.1, lx=0, ly=0):
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#5A5A5A", lw=0.8,
                solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=7.5,
                                 linewidth=0.8, color="#5A5A5A"))
    if label:
        mx, my = pts[len(pts) // 2][0] + lx, pts[len(pts) // 2][1] + ly
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color="#333333", bbox=dict(fc="white", ec="none", pad=0.7))


# ---------------------------------------------------------------- Figure 3.1
def architecture():
    fig, ax = canvas(9.2, 3.5, 184, 98)
    ax.set_ylim(3, 71)

    box(ax, 2, 24, 26, 44, "", GREY_FC, GREY_EC, rounded=1.2)
    ax.text(15, 63.5, "Users / Entry Points", ha="center", va="center",
            fontsize=6.2, fontweight="bold")
    box(ax, 5, 52, 20, 6.4, "Passenger", BLUE_FC, fs=7.0)
    box(ax, 5, 40, 20, 6.4, "Driver", BLUE_FC, fs=7.0)
    box(ax, 5, 28, 20, 6.4, "Administrator", BLUE_FC, fs=6.3)

    box(ax, 32, 38, 44, 30, "", BLUE_FC, BLUE_EC, rounded=1.2)
    ax.text(54, 64.2, "Presentation Layer", ha="center", va="center", fontsize=7.6, fontweight="bold")
    ax.text(54, 55.5, "Vue 3 SPA  \u2022  Vue Router\nVite  \u2022  Tailwind CSS\nPinia stores  \u2022  RideMap component",
            ha="center", va="center", fontsize=7.0, color=TEXT, linespacing=1.45)

    box(ax, 84, 38, 46, 30, "", TAN_FC, TAN_EC, rounded=1.2)
    ax.text(107, 64.2, "Application Layer", ha="center", va="center", fontsize=7.6, fontweight="bold")
    ax.text(107, 52, "FastAPI  \u2022  Pydantic  \u2022  Uvicorn\n/api/rides  /api/drivers\n/api/passengers  /api/dsa\nMatchmaking Service",
            ha="center", va="center", fontsize=7.0, color=TEXT, linespacing=1.4)

    box(ax, 84, 6, 46, 22, "", GREY_FC, GREY_EC, rounded=1.2)
    ax.text(107, 23.5, "Data Structures & Algorithms Layer", ha="center", va="center",
            fontsize=7.2, fontweight="bold")
    ax.text(107, 13.6, "Singly Linked List  \u2022  FIFO Queue\nBinary Min-Heap Priority Queue\nLIFO Stack  \u2022  Chained Hash Table",
            ha="center", va="center", fontsize=6.9, color=TEXT, linespacing=1.4)

    box(ax, 140, 38, 40, 30, "", BLUE_FC, BLUE_EC, rounded=1.2)
    ax.text(160, 64.2, "Data Storage Layer", ha="center", va="center", fontsize=7.6, fontweight="bold")
    ax.text(160, 52, "SQLite (bundled)\nPostgreSQL fallback\npassengers / rides",
            ha="center", va="center", fontsize=7.0, color=TEXT, linespacing=1.45)

    box(ax, 32, 6, 44, 22, "", TAN_FC, TAN_EC, rounded=1.2)
    ax.text(54, 23.5, "Map & Routing Services", ha="center", va="center", fontsize=7.4, fontweight="bold")
    ax.text(54, 13.6, "Leaflet map canvas\nEsri World Dark Gray tiles\nOSRM road routing",
            ha="center", va="center", fontsize=7.0, color=TEXT, linespacing=1.45)

    arrow(ax, (28, 55), (31.4, 55), "HTTPS", ly=13.5, lx=1.5)
    arrow(ax, (76.4, 55), (83.4, 55), "REST / JSON", ly=2.6)
    arrow(ax, (130.4, 55), (139.4, 55), "SQL", ly=2.6)
    arrow(ax, (107, 37.6), (107, 28.6), "function calls", lx=10, ly=0)
    arrow(ax, (76.4, 22), (83.4, 22), "coords", lx=0, ly=2.3)
    arrow(ax, (54, 27.8), (54, 37.6), "tiles / routes", lx=11.5, ly=0)

    fig.savefig(os.path.join(OUT, "fig-3-1-architecture.png"), facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3.2
def usecase():
    fig, ax = canvas(7.2, 8.8, 112, 140)

    ax.add_patch(Rectangle((44, 2), 66, 134, fill=False, edgecolor="#8FB3D9", linewidth=1.0))
    ax.text(77, 130, "Pink Wheels", ha="center", va="center", fontsize=8.4, fontweight="bold")

    def actor(x, y, label):
        ax.add_patch(plt.Circle((x, y + 4.6), 1.9, fill=False, ec="#333333", lw=0.9))
        ax.plot([x, x], [y + 2.7, y - 2.2], color="#333333", lw=0.9)
        ax.plot([x - 3, x, x + 3], [y + 0.6, y + 1.6, y + 0.6], color="#333333", lw=0.9)
        ax.plot([x - 2.6, x, x + 2.6], [y - 6, y - 2.2, y - 6], color="#333333", lw=0.9)
        ax.text(x, y - 8.8, label, ha="center", va="center", fontsize=7.2, fontweight="bold")

    actor(16, 112, "Passenger")
    actor(16, 70, "Driver")
    actor(16, 24, "Administrator")

    def oval(y, text, w=58, h=8.0, fs=6.9):
        ax.add_patch(Ellipse((77.5, y), w, h, facecolor=BLUE_FC, edgecolor=BLUE_EC, lw=0.9))
        ax.text(77.5, y, text, ha="center", va="center", fontsize=fs, color=TEXT)

    for y, text in [(120, "Select passenger identity"), (109, "Request a ride"),
                    (98, "View fare estimate"), (87, "Track ride status"),
                    (76, "View ride history")]:
        oval(y, text)
        ax.plot([20.5, 48.4], [112, y], color="#A6A6A6", lw=0.7)

    for y, text in [(63, "View offered ride"), (52, "Accept / reject offer"),
                    (41, "Complete trip"), (30, "Update availability")]:
        oval(y, text)
        ax.plot([20.5, 48.4], [70, y], color="#A6A6A6", lw=0.7)

    for y, text in [(16, "Inspect data structures"), (6.5, "Run matchmaking simulation")]:
        oval(y, text, fs=6.6)
        ax.plot([20.5, 48.4], [24, y], color="#A6A6A6", lw=0.7)

    fig.savefig(os.path.join(OUT, "fig-3-2-usecase.png"), facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3.3
def dfd_context():
    fig, ax = canvas(8.6, 3.8, 172, 84)
    ax.set_ylim(5, 82)

    ax.add_patch(Ellipse((86, 42), 46, 30, facecolor=BLUE_FC, edgecolor=BLUE_EC, lw=1.0))
    ax.text(86, 47, "0", ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(86, 40.5, "Pink Wheels", ha="center", va="center", fontsize=8.2, fontweight="bold")
    ax.text(86, 34.5, "Ride Management", ha="center", va="center", fontsize=7.6)

    rect(ax, 4, 56, 30, 13, "Passenger", TAN_FC, TAN_EC, 7.6)
    rect(ax, 4, 15, 30, 13, "Driver", TAN_FC, TAN_EC, 7.6)
    rect(ax, 138, 36, 32, 13, "Administrator", TAN_FC, TAN_EC, 7.4)

    arrow(ax, (34, 62), (64, 50), "ride request, cancel", ly=3.4)
    poly_arrow(ax, [(86, 57), (86, 76), (19, 76), (19, 69.4)],
               "fare, driver, status", lx=40, ly=2.4)
    arrow(ax, (34, 25), (66, 33), "availability, decision", ly=3.2)
    poly_arrow(ax, [(86, 27), (86, 10), (19, 10), (19, 14.6)],
               "offer details", lx=32, ly=-2.8)
    arrow(ax, (108, 45), (137, 43), "query", ly=4.4)
    arrow(ax, (137, 38), (108, 37), "snapshots", ly=-4.6)

    fig.savefig(os.path.join(OUT, "fig-3-3-dfd-context.png"), facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3.4
def dfd_level1():
    fig, ax = canvas(9.0, 5.9, 180, 124)
    ax.set_ylim(4, 122)

    rect(ax, 2, 96, 28, 13, "Passenger", TAN_FC, TAN_EC, 7.2)
    rect(ax, 2, 62, 28, 13, "Driver", TAN_FC, TAN_EC, 7.2)
    rect(ax, 92, 8, 32, 11, "Administrator", TAN_FC, TAN_EC, 7.0)

    box(ax, 36, 96, 34, 14, "1\nPassenger\nManagement", BLUE_FC, BLUE_EC, 6.9)
    box(ax, 92, 96, 34, 14, "2\nFare\nEstimation", BLUE_FC, BLUE_EC, 6.9)
    box(ax, 36, 62, 34, 14, "3\nRide Intake &\nQueueing", BLUE_FC, BLUE_EC, 6.9)
    box(ax, 92, 62, 34, 14, "4\nDriver\nMatchmaking", BLUE_FC, BLUE_EC, 6.9)
    box(ax, 36, 28, 34, 14, "5\nOffer\nLifecycle", BLUE_FC, BLUE_EC, 6.9)
    box(ax, 92, 28, 34, 14, "6\nDSA\nDemonstration", BLUE_FC, BLUE_EC, 6.9)

    def store(x, y, w, label, fs=6.4):
        ax.add_patch(Rectangle((x, y), w, 8, facecolor=GREY_FC, edgecolor=GREY_EC, lw=0.9))
        ax.plot([x + 4, x + 4], [y, y + 8], color=GREY_EC, lw=0.8)
        ax.text(x + 4 + (w - 4) / 2, y + 4, label, ha="center", va="center", fontsize=fs)

    store(136, 96, 36, "D1  passengers")
    store(136, 62, 36, "D3  in-memory structures", 5.9)
    store(136, 28, 36, "D2  rides")

    # passenger row
    arrow(ax, (30, 105), (35.6, 105), "ride request", ly=7.4)
    arrow(ax, (36, 100), (30.4, 100), "fare, status", ly=-7.2)
    arrow(ax, (70, 105), (91.6, 105), "validated request", ly=7.4)
    arrow(ax, (92, 100), (70.4, 100), "fare quote", ly=-7.2)
    arrow(ax, (60, 96), (60, 76.4), "session", lx=7.5, ly=0)
    poly_arrow(ax, [(48, 110), (48, 117), (150, 117), (150, 104.6)],
               "INSERT", lx=-14, ly=2.4)

    # driver row
    arrow(ax, (30, 69), (35.6, 69), "availability", ly=8.2)
    arrow(ax, (36, 65), (30.4, 65), "offer, trip", ly=-7.2)
    arrow(ax, (70, 69), (91.6, 69), "queued ride", ly=7.4)
    arrow(ax, (126, 69), (135.6, 69), "heap state", ly=3.6)
    arrow(ax, (136, 64), (126.4, 64), "candidates", ly=-5.6)
    poly_arrow(ax, [(92, 66), (84, 66), (84, 35), (70, 35)],
               "offer top candidate", lx=13.5, ly=15)
    arrow(ax, (48, 42), (48, 61.6), "reassign", lx=9.5, ly=0)
    poly_arrow(ax, [(62, 28), (62, 22), (150, 22), (150, 27.4)],
               "status write", lx=-80, ly=0)

    # DSA row
    arrow(ax, (126, 35), (135.6, 35), "ride list", ly=4.4)
    arrow(ax, (108, 19), (108, 27.4), "inspect", lx=-11, ly=0)
    arrow(ax, (120, 27.4), (120, 19), "snapshot", lx=11, ly=0)

    fig.savefig(os.path.join(OUT, "fig-3-4-dfd-level1.png"), facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- Figure 3.5
def flowchart():
    fig, ax = canvas(5.8, 6.8, 156, 180)

    cx = 58
    w = 64
    x0 = cx - w / 2

    box(ax, cx - 24, 168, 48, 9, "Start: ride request received",
        BLUE_FC, BLUE_EC, 7.2, rounded=4.5, bold=True)
    box(ax, x0, 151, w, 11, "Traverse driver linked list;\nkeep available, non-excluded drivers",
        GREY_FC, GREY_EC, 6.9)
    box(ax, x0, 134, w, 11, "Compute Haversine distance and ETA\nfor each eligible candidate",
        GREY_FC, GREY_EC, 6.9)
    box(ax, x0, 117, w, 11, "Push each candidate into the\nbinary min-heap priority queue",
        GREY_FC, GREY_EC, 6.9)
    box(ax, x0, 103, w, 9.5, "Pop root candidate  (O(log n))", GREY_FC, GREY_EC, 6.9)
    diamond(ax, cx, 89.5, 40, 14, "Candidate\nexists?", "#FFFFFF", "#9A9A9A", 6.8)
    box(ax, x0, 66, w, 9.5, "Offer ride; status becomes OFFERED", GREY_FC, GREY_EC, 6.9)
    diamond(ax, cx, 55, 40, 14, "Driver\naccepts?", "#FFFFFF", "#9A9A9A", 6.8)
    diamond(ax, cx, 35, 40, 14, "Heap\nempty?", "#FFFFFF", "#9A9A9A", 6.8)

    # terminal boxes
    box(ax, 1, 48, 30, 14, "Status\nNO_DRIVERS_\nAVAILABLE", TAN_FC, TAN_EC, 6.4)
    box(ax, 100, 48, 30, 14, "Mark driver busy;\nstatus ACCEPTED", TAN_FC, TAN_EC, 6.3)
    ax.add_patch(Ellipse((58, 8), 24, 10, facecolor=BLUE_FC, edgecolor=BLUE_EC, lw=0.9))
    ax.text(58, 8, "End", ha="center", va="center", fontsize=7.4, fontweight="bold")

    arrow(ax, (cx, 168), (cx, 162.4))
    arrow(ax, (cx, 151), (cx, 145.4))
    arrow(ax, (cx, 134), (cx, 128.4))
    arrow(ax, (cx, 117), (cx, 112.9))
    arrow(ax, (cx, 103), (cx, 96.9))
    arrow(ax, (cx, 82.5), (cx, 75.9), "yes", lx=5, ly=0)
    arrow(ax, (cx, 66), (cx, 62.4))
    arrow(ax, (cx, 48), (cx, 42.4), "no", lx=4.5, ly=0)

    # candidate absent -> terminal
    poly_arrow(ax, [(38, 89.5), (16, 89.5), (16, 62.6)], "no", lx=-1, ly=2.6)
    # heap empty -> same terminal
    poly_arrow(ax, [(38, 35), (16, 35), (16, 47.4)], "yes", lx=-1, ly=2.6)
    # terminal -> end
    poly_arrow(ax, [(16, 48), (16, 8), (45.6, 8)])
    # accepted -> end
    poly_arrow(ax, [(130, 55), (145, 55), (145, 8), (70.4, 8)])
    # accepted branch
    arrow(ax, (78, 55), (99.6, 55), "yes", lx=0, ly=2.8)
    # heap not empty -> pop next candidate
    poly_arrow(ax, [(78, 35), (136, 35), (136, 107.8), (90.4, 107.8)],
               "no \u2014 pop next candidate", lx=-24, ly=-3.2)

    fig.savefig(os.path.join(OUT, "fig-3-5-matchmaking-flowchart.png"), facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    usecase()
    dfd_context()
    dfd_level1()
    flowchart()
    print("diagrams written to", OUT)
