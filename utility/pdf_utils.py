import numpy as np
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Rectangle
from matplotlib.ticker import PercentFormatter

matplotlib.rc("figure", dpi=200)


def isNaN(input):
    return input != input

def plot_to_html(fig):
    sunalt = fig
    buf = io.BytesIO()
    sunalt.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    b2 = base64.b64encode(buffer)
    sunalt2 = b2.decode('utf-8')
    return sunalt2


def format_graph(df, title, font_type):  # from DataFrame format
    matplotlib.rc('font', family=font_type)
    n_colors = df.shape[1]
    colors = plt.cm.jet(np.linspace(0, 1, n_colors))
    ax = df.plot(color=colors, title=title, rot=45, figsize=(17, 7), fontsize=25)
    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=25, labelcolor=color_theme)
    ax.set_title(title, fontdict={'fontsize': 30, 'fontweight': 'medium', 'color': color_theme})
    ax.tick_params(axis='x', colors=color_theme)
    ax.tick_params(axis='y', colors=color_theme)
    #for line in ax.get_lines():
    #    line.set_linewidth(10)
    plt.tight_layout()
    return ax


def format_graph_3(df, title, font_type, _font_size=25, _title_size=30, _fig_size=(17, 7)):  # from DataFrame format
    matplotlib.rc('font', family=font_type)
    n_colors = df.shape[1]
    colors = plt.cm.jet(np.linspace(0, 1, n_colors))
    ax = df.plot(color=colors, title=title, rot=45, figsize=_fig_size, fontsize=_font_size)

    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=_font_size, labelcolor=color_theme)
    if title is not None:
        ax.set_title(title, fontdict={'fontsize': _title_size, 'fontweight': 'medium', 'color': color_theme})

    ax.tick_params(axis='x', colors=color_theme)
    ax.tick_params(axis='y', colors=color_theme)

    for line in ax.get_lines():
        line.set_linewidth(0.5)

    plt.tight_layout()
    return ax


def format_graph_2(df, font_type):  # from DataFrame format
    matplotlib.rc('font', family=font_type)
    n_colors = df.shape[1]
    colors = plt.cm.jet(np.linspace(0, 1, n_colors))
    ax = df.plot(color=colors, rot=45, figsize=(17, 9), fontsize=25)
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=25, labelcolor=color_theme)
    ax.tick_params(axis='x', colors=color_theme)
    ax.tick_params(axis='y', colors=color_theme)
    plt.tight_layout()
    return ax

def format_graph_4(df, font_type, fig_size=(17, 9)):  # from DataFrame format
    matplotlib.rc('font', family=font_type)
    n_colors = df.shape[1]
    colors = plt.cm.jet(np.linspace(0, 0.75, n_colors))
    ax = df.plot(color=colors, rot=45, figsize=fig_size, fontsize=25)
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=15, labelcolor=color_theme)
    ax.tick_params(axis='x', colors=color_theme)
    ax.tick_params(axis='y', colors=color_theme)
    plt.tight_layout()
    return ax

#ncol=df.shape[1]+1

def formatted_bar_chart(x_values, y_values, x_label=None, y_label=None, title=None, bar_color="blue", angle=0):
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    fig, ax = plt.subplots(figsize=(18, 6.8))
    plt.bar(x_values, y_values, color=bar_color)
    if not isNaN(y_label):
        plt.ylabel(y_label, fontname="Cambria", fontsize=25, color=color_theme)  # set the labels of x-axis and y-axis
    if not isNaN(x_label):
        plt.xlabel(x_label, fontname="Cambria", fontsize=25, color=color_theme)
    plt.xticks(fontname="Cambria", color=color_theme, rotation=angle, fontsize=25)
    plt.yticks(fontname="Cambria", color=color_theme, fontsize=25)
    if not isNaN(title):
        plt.title(title, fontname="Cambria", color=color_theme, fontsize=25)
    plt.tight_layout()
    ax_output = plt.gca()
    return ax_output


def formatted_scatter_plot(df, x_col, y_col, font_type, dot_color="blue", fig_size=(5, 6.1), angle=0):  # from DataFrame format
    matplotlib.rc('font', family=font_type)
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    ax = df.plot.scatter(x=x_col, y=y_col, c=dot_color, figsize=fig_size, fontsize=22, s=35)
    plt.xticks(color=color_theme, fontsize=18, rotation=angle)
    plt.yticks(color=color_theme, fontsize=18)
    plt.xlabel(x_col, color=color_theme, fontsize=20)
    plt.ylabel(y_col, color=color_theme, fontsize=20)
    ax.axhline()
    plt.tight_layout()
    return ax


def formatted_box_plot(df, font_type, plot_title, x_lab, face_colors=['blue'], median_color='red', fig_size=(17.6, 8.10)):
    matplotlib.rc('font', family=font_type)
    color_theme = (0 / 235, 32 / 235, 96 / 235)
    data = np.array(df)
    fig, ax = plt.subplots(figsize=fig_size)
    bp = plt.boxplot(data, patch_artist=True)

    if len(face_colors) != df.shape[0]:
        colors = [face_colors[0]] * df.shape[0]
    else:
        colors = plt.cm.jet(np.linspace(0, 1, df.shape[0]))

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    for whisker in bp['whiskers']:
        whisker.set(color='#8B008B',
                    linewidth=1.5,
                    linestyle=":")
    for cap in bp['caps']:
        cap.set(color='#8B008B',
                linewidth=2)
    for median in bp['medians']:
        median.set(color=median_color,
                   linewidth=3)

    for flier in bp['fliers']:
        flier.set(marker='D',
                  color='#e7298a',
                  alpha=0.5)
    plt.xlabel(x_lab, color=color_theme, fontsize=20)
    plt.xticks(rotation=45, color=color_theme, fontsize=20)
    plt.yticks(color=color_theme, fontsize=20)
    ax.set_xticklabels(df.columns.to_list())
    plt.title(plot_title, color=color_theme, fontsize=25)
    plt.grid(color='#808080', linestyle='-', linewidth=1)
    plt.tight_layout()
    return ax  # plt.gca()


def formatted_pie_chart(df, explode=None, _col=None, tsize=14):
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc('font', family="Cambria")
    if isinstance(df, pd.DataFrame):
        vals = df.iloc[0,:].values.tolist()
        labels = df.columns
    elif isinstance(df, pd.Series):
        vals = df.values.tolist()
        labels = df.index
    else:
        vals = list(df)
        labels = ["GROUP {}".format(i) for i in range(len(vals))]

    if _col is not None and max([i for _c in _col for i in _c]) > 1:
        _col = [(_c[0]/255, _c[1]/255, _c[2]/255) for _c in _col]

    fig1, ax1 = plt.subplots()
    _, texts, autotexts = ax1.pie(vals, explode=explode,
                                  labels=labels,
                                  autopct='%1.1f%%',
                                  pctdistance=0.90,
                                  labeldistance=1.02,
                                  shadow=False,
                                  startangle=45,
                                  colors=_col)

    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    for at in autotexts:
        at.set_color("white")
        at.set_font("Cambria")

    for t in texts:
        t.set_color((0 / 235, 32 / 235, 96 / 235))
        t.set_font("Cambria")
        t.set_size(tsize)

    plt.rcParams.update({"savefig.transparent": True})
    return ax1


def formatted_stacked_chart(df, _col=None, add_legend=False):
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc('font', family="Cambria")
    if isinstance(df, pd.DataFrame):
        color_theme = (0 / 235, 32 / 235, 96 / 235)

        if _col is not None and max([i for _c in _col for i in _c]) > 1:
            _col = [(_c[0] / 255, _c[1] / 255, _c[2] / 255) for _c in _col]

        x = df.index.values
        vals = []
        labels = []
        for _c in range(len(df.columns)):
            labels.append(df.columns[_c])
            vals.append(df.iloc[:,_c].values)

        fig1, ax1 = plt.subplots()
        fields = ax1.stackplot(x, *vals, labels=labels, colors=_col)

        ax1.spines['bottom'].set_color(color_theme)
        ax1.spines['top'].set_color(color_theme)
        ax1.spines['right'].set_color(color_theme)
        ax1.spines['left'].set_color(color_theme)

        ax1.tick_params(axis='x', colors=color_theme)
        ax1.tick_params(axis='y', colors=color_theme)

        if add_legend:
            colors = [field.get_facecolor()[0] for field in fields]
            patches = []
            for _i in range(len(colors)):
                patches.append(matplotlib.patches.Patch(color=colors[_i], label=labels[_i]))

            plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=len(colors),
                       labelcolor=color_theme, frameon=False)

        plt.rcParams.update({"savefig.transparent": True})
        plt.tight_layout()

        return ax1
    else:
        return None


def bars_autolabel(_rects_series, _ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in _rects_series:
        height = rect.get_height()
        _ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def formatted_multiple_bar_chart(df, _col=None, nums_on_bars=False, width=0.8, perc=False):
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc('font', family="Cambria")
    if isinstance(df, pd.DataFrame):
        color_theme = (0 / 235, 32 / 235, 96 / 235)

        if _col is not None and max([i for _c in _col for i in _c]) > 1:
            _col = [(_c[0] / 255, _c[1] / 255, _c[2] / 255) for _c in _col]

        fig1, ax1 = plt.subplots()
        rects = []
        labels = df.index.values
        x = np.arange(len(labels))
        # TODO handle positions
        width_part = width / len(df.columns)

        for _i in range(len(df.columns)):
            vals = df.iloc[:, _i].values
            bar_kwargs = {"label": df.columns[_i]}
            if _col is not None:
                bar_kwargs["color"] = _col[_i] if len(_col) == len(df.columns) else _col

            rects.append(ax1.bar(x - ((width-width_part)/2) + _i * width_part, vals, width_part, **bar_kwargs))
            if nums_on_bars:
                bars_autolabel(rects[_i])

        if perc:
            ax1.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)

        ax1.spines['bottom'].set_color(color_theme)
        ax1.spines['top'].set_color(color_theme)
        ax1.spines['right'].set_color(color_theme)
        ax1.spines['left'].set_color(color_theme)

        ax1.tick_params(axis='x', colors=color_theme)
        ax1.tick_params(axis='y', colors=color_theme)

        ax1.legend(labelcolor=color_theme, loc='upper center', bbox_to_anchor=(0.5, -0.05),
                   ncol=len(df.columns), frameon=False)

        plt.tight_layout()
        return ax1


def autoformatted_bar_chart(df, _col=None, _fig_size=(15, 10), _hl=None, fsize=6, _perc=False):
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc('font', family="Cambria")

    if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
        _df = df.to_frame().copy() if isinstance(df, pd.Series) else df.copy()
        _df = _df.loc[:, _df.columns[0]]
        color_theme = (0 / 255, 32 / 255, 96 / 255)

        if _col is not None and max([i for _c in _col for i in _c]) > 1:
            _col = [(_c[0] / 255, _c[1] / 255, _c[2] / 255) for _c in _col]

        colors = _col if (_col is not None) and (len(_df.index) == len(_col))\
                                    else [color_theme] * (len(_df.index))

        my_plot = _df.plot(kind='bar', stacked=False, legend=None, figsize=_fig_size, color=colors)
        my_plot.set_xticklabels(_df.index, rotation=45, fontsize=fsize)

        if _hl is not None:
            for i in range(_hl):
                if i < len(my_plot.get_children()) and isinstance(my_plot.get_children()[i], Rectangle):
                    my_plot.get_children()[i].set_edgecolor((68/255, 228/255, 250/255))

        fig = my_plot.get_figure()
        fig.tight_layout()
        fig.axes[0].spines['bottom'].set_color(color_theme)
        fig.axes[0].spines['top'].set_color(color_theme)
        fig.axes[0].spines['right'].set_color(color_theme)
        fig.axes[0].spines['left'].set_color(color_theme)

        if _perc:
            fig.axes[0].yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

        return fig


def double_bar_chart(df_up, df_down, _col=None, _fig_size=(15, 10), fsize=8, names=(None, None), perc=True):
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc('font', family="Cambria")

    assert all([df_up.index[i] == df_down.index[i] for i in range(len(df_down.index))]), "Vertical Stacking impossible"

    if isinstance(df_up, pd.Series) and isinstance(df_down, pd.Series) :
        x_scalar = range(len(df_up.index))
        color_theme = (0 / 255, 32 / 255, 96 / 255)

        if _col is not None and max([i for _c in _col for i in _c]) > 1:
            _col = [(_c[0] / 255, _c[1] / 255, _c[2] / 255) for _c in _col]

        colors = _col if (_col is not None) and (len(df_up.index) == len(_col))\
                                    else [color_theme] * (len(df_up.index))

        fig, (ax1, ax2) = plt.subplots(2)
        ax1.bar(x=x_scalar, height=df_up.values, color=colors, align='edge')
        if names[0] is not None:
            ax1.set(ylabel=names[0])

        ax2.bar(x=x_scalar, height=df_down.values, color=colors, align='edge')
        if names[1] is not None:
            ax2.set(ylabel=names[1])

        for ax in (ax1, ax2):
            ax.label_outer()

        plt.xticks(x_scalar, df_up.index.values, rotation=45, color=color_theme)

        if perc:
            ax1.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
            ax2.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

        ax1.tick_params(axis='x', colors=color_theme, labelsize=fsize)
        ax1.tick_params(axis='y', colors=color_theme, labelsize=fsize)
        ax2.tick_params(axis='x', colors=color_theme, labelsize=fsize)
        ax2.tick_params(axis='y', colors=color_theme, labelsize=fsize)

        fig.tight_layout()
        ax1.spines['bottom'].set_color(color_theme)
        ax1.spines['top'].set_color(color_theme)
        ax1.spines['right'].set_color(color_theme)
        ax1.spines['left'].set_color(color_theme)
        ax2.spines['bottom'].set_color(color_theme)
        ax2.spines['top'].set_color(color_theme)
        ax2.spines['right'].set_color(color_theme)
        ax2.spines['left'].set_color(color_theme)

        return fig


def formatted_multiple_scatter_chart(df, _col=None, nums_on_bars=False, width=0.8):
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc('font', family="Cambria")
    if isinstance(df, pd.DataFrame):
        color_theme = (0 / 235, 32 / 235, 96 / 235)

        if _col is not None and max([i for _c in _col for i in _c]) > 1:
            _col = [(_c[0] / 255, _c[1] / 255, _c[2] / 255) for _c in _col]

        fig1, ax1 = plt.subplots()
        x = df.index.values

        for _i in range(len(df.columns)):
            y = df.iloc[:, _i].values
            if _col is not None:
                color = _col[_i] if len(_col) == len(df.columns) else _col
            else:
                color=None

            ax1.scatter(x, y, c=color, s=100.0, label=df.columns[_i], alpha=0.3, edgecolors='none')


        ax1.spines['bottom'].set_color(color_theme)
        ax1.spines['top'].set_color(color_theme)
        ax1.spines['right'].set_color(color_theme)
        ax1.spines['left'].set_color(color_theme)

        ax1.tick_params(axis='x', colors=color_theme, labelsize=7)
        ax1.tick_params(axis='y', colors=color_theme)

        ax1.legend(labelcolor=color_theme, loc='upper center', bbox_to_anchor=(0.5, -0.1),
                   ncol=len(df.columns), frameon=False)
        # ax1.legend(labelcolor=color_theme, n_cols)

        plt.tight_layout()
        # plt.margins(5, 0, tight=False)
        return ax1


# Input: a Series/Dataframe with labels as index and the values (negative or positive),
# the name of the series is used as name of the unit

def formatted_waterfall_chart(df, _col=None, recap_field_name="net", rf_color=None, _fig_size=(10, 15), _f=6):
    matplotlib.rc('font', family="Cambria")
    matplotlib.rc('lines', color=(0 / 255, 32 / 255, 96 / 255))
    matplotlib.rc("figure", dpi=200)
    matplotlib.rc("text", color=(0 / 255, 32 / 255, 96 / 255))
    matplotlib.rc("xtick", color=(0 / 255, 32 / 255, 96 / 255))
    matplotlib.rc("ytick", color=(0 / 255, 32 / 255, 96 / 255))

    if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
        _df = df.to_frame().copy() if isinstance(df, pd.Series) else df.copy()
        _df = _df.loc[:, _df.columns[0]]
        color_theme = (0 / 255, 32 / 255, 96 / 255)
        rf_color = color_theme if rf_color is None else (rf_color[0]/255, rf_color[1]/255, rf_color[2]/255)

        if _col is not None and max([i for _c in _col for i in _c]) > 1:
            _col = [(_c[0] / 255, _c[1] / 255, _c[2] / 255) for _c in _col]

        colors = _col + [rf_color] if (_col is not None) and (len(_df.index) == len(_col))\
                                    else [color_theme] * (len(_df.index)) + [rf_color]


        # Store data and create a blank series to use for the waterfall
        blank = _df.cumsum().shift(1).fillna(0)

        # Get the net total number for the final element in the waterfall
        total = _df.sum()
        _df.loc[recap_field_name] = total
        blank.loc[recap_field_name] = total

        # The steps graphically show the levels as well as used for label placement
        step = blank.reset_index(drop=True).repeat(3).shift(-1)
        step[1::3] = np.nan

        # When plotting the last element, we want to show the full bar,
        # Set the blank to 0
        blank.loc[recap_field_name] = 0

        # Plot and label
        my_plot = _df.plot(kind='bar', stacked=True, bottom=blank, legend=None,
                           figsize=_fig_size, color=colors)
        my_plot.plot(step.index, step.values, 'k', lw=0.5)

        # Get the y-axis position for the labels
        y_height = _df.cumsum().shift(1).fillna(0).values.tolist()

        # Get an offset so labels don't sit right on top of the bar
        maximum = _df.max()
        neg_offset = maximum / 20
        pos_offset = maximum / 50
        plot_offset = int(maximum / 15)

        # Start label loop
        loop = 0
        for i in range(len(_df)):
            row = _df.iloc[i]
            # For the last item in the list, we don't want to double count
            if row == total:
                y = y_height[loop]
            else:
                y = y_height[loop] + row
            # Determine if we want a neg or pos offset
            if row > 0:
                y += pos_offset
            else:
                y -= neg_offset
            my_plot.annotate("{:,.0f}".format(row), (loop, y), ha="center", fontsize=8)
            loop = loop + 1

        # Scale up the y axis so there is room for the labels
        my_plot.set_ylim(0, blank.max() + int(plot_offset))
        # Rotate the labels
        my_plot.set_xticklabels(_df.index, rotation=45, fontsize=8)
        fig = my_plot.get_figure()
        fig.tight_layout()
        fig.axes[0].spines['top'].set_visible(False)
        fig.axes[0].spines['right'].set_visible(False)

        return fig


def print_placeholders_structure(prs):
    for sm in prs.slide_masters:
        for sl in sm.slide_layouts:
            for shape in sl.placeholders:
                print('%s %s %d %s %d %d %s' % (sm.name, sl.name, shape.placeholder_format.idx,
                                                shape.name, shape.height, shape.width, shape.text))