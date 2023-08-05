"""Tkinter GUI code."""


import os
import sys
import json
import logging
import threading

import dtoolcore.utils

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from dtool_gui_tk.models import (
    LocalBaseURIModel,
    DataSetListModel,
    DataSetModel,
    ProtoDataSetModel,
    MetadataSchemaListModel,
    UnsupportedTypeError,
)

logger = logging.getLogger(__file__)

CONFIG_DIR = os.path.dirname(dtoolcore.utils.DEFAULT_CONFIG_PATH)
METADATA_SCHEMAS_DIR = os.path.join(CONFIG_DIR, "metadata_schemas")
HOME_DIR = os.path.expanduser("~")

# Create the metadata schemas directory if it does not exist.
dtoolcore.utils.mkdir_parents(METADATA_SCHEMAS_DIR)


# Make sure a basic metadata schema is present in the metadata schemas
# directory.
_basic_schema = {
    "type": "object",
    "properties": {
        "description": {
            "type": "string"
        }
    },
    "required": ["description"]
}
_basic_schema_fpath = os.path.join(METADATA_SCHEMAS_DIR, "basic.json")
if not os.path.isfile(_basic_schema_fpath):
    with open(_basic_schema_fpath, "w") as fh:
        json.dump(_basic_schema, fh)


def _set_combobox_default_selection(combobox, choices, selected):
    index = None
    if selected is not None:
        index = choices.index(str(selected))
    if index is not None:
        combobox.current(index)


class DataSetListFrame(ttk.Frame):
    """List dataset frame."""

    def __init__(self, master, root):
        super().__init__(master)
        logger.info("Initialising {}".format(self))

        # Make sure that the GUI expands/shrinks when the window is resized.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.root = root
        self.columns = ("name", "size_str", "num_items", "creator", "date")
        self.dataset_list = ttk.Treeview(
            self,
            show="headings",
            height=10,
            selectmode="browse",
            columns=self.columns
        )
        self.dataset_list.heading("name", text="Dataset name")
        self.dataset_list.heading("size_str", text="Size")
        self.dataset_list.heading("num_items", text="Num items")
        self.dataset_list.heading("creator", text="Creator")
        self.dataset_list.heading("date", text="Date")
        self.dataset_list.column("size_str", width=80, anchor="e")
        self.dataset_list.column("num_items", width=80, anchor="e")
        self.dataset_list.column("creator", width=80, anchor="w")
        self.dataset_list.column("date", width=80, anchor="w")

        # Add a scrollbar.
        yscrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.dataset_list.yview
        )
        self.dataset_list.configure(yscroll=yscrollbar.set)

        # Bind event when row is selected.
        self.dataset_list.bind(
            "<<TreeviewSelect>>",
            self.update_selected_dataset
        )

        # Layout the fame.
        self.dataset_list.grid(row=0, column=0, sticky="nswe")
        yscrollbar.grid(row=0, column=1, sticky="ns")

        self.refresh()

    def update_selected_dataset(self, event):
        selected = self.dataset_list.selection()[0]
        index = self.dataset_list.index(selected)
        dataset_uri = self.root.dataset_list_model.get_uri(index)
        self.root.load_dataset(dataset_uri)
        self.root.dataset_frame.refresh()

    def refresh(self):
        """Refresh list dataset frame."""
        logger.info("Refreshing {}".format(self))
        self.dataset_list.delete(*self.dataset_list.get_children())
        self.root.dataset_list_model.reindex()
        for props in self.root.dataset_list_model.yield_properties():
            values = [props[c] for c in self.columns]
            self.dataset_list.insert("", "end", values=values)
            logger.info("Loaded dataset: {}".format(props["name"]))
        if len(self.root.dataset_list_model.names) > 0:
            dataset_uri = self.root.dataset_list_model.get_uri(0)
            self.root.load_dataset(dataset_uri)
        else:
            self.root.dataset_model.clear()


class DataSetFrame(ttk.Frame):
    """View dataset frame."""

    def __init__(self, master, root):
        super().__init__(master)
        logger.info("Initialising {}".format(self))

        # Make sure that the GUI expands/shrinks when the window is resized.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.root = root
        if self.root.base_uri_model.get_base_uri() is not None:
            self.refresh()

    def refresh(self):
        """Refreshing dataset frame."""
        logger.info("Refreshing {}".format(self))
        for widget in self.winfo_children():
            logger.info("Destroying widget: {}".format(widget))
            widget.destroy()

        # Skip if a dataset is not loaded.
        if self.root.dataset_model.name is None:
            return

        # Display the name.
        name = ttk.Label(self, text=self.root.dataset_model.name)  # NOQA
        name.grid(row=0, column=0, columnspan=2, sticky="nw")
        separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        separator.grid(row=1, column=0, columnspan=2, sticky="ew")

        if self.root.dataset_model.metadata_model is None:
            ttk.Label(self, text="Dataset contains unsupported metadata types").grid(row=2, column=0, columnspan=2, sticky="ew")  # NOQA

        else:
            for i, name in enumerate(self.root.dataset_model.metadata_model.in_scope_item_names):  # NOQA
                value = self.root.dataset_model.metadata_model.get_value(name)
                value_as_str = str(value)
                row = i + 2
                ttk.Label(self, text=name).grid(row=row, column=0, sticky="e")  # NOQA
                entry = ttk.Entry(self, width=50)
                entry.insert(0, value_as_str)
                entry.configure(state="readonly")
                entry.grid(row=row, column=1, sticky="w")  # NOQA


class NewDataSetConfigFrame(ttk.Frame):
    """New dataset configuration frame."""

    def __init__(self, master, root):
        super().__init__(master)
        logger.info("Initialising {}".format(self))
        self.master = master
        self.root = root
        self.label_frame = ttk.LabelFrame(self, text="New dataset configuration")  # NOQA
        self.label_frame.grid(row=0, column=0, sticky="nsew")
        self.refresh()

    def _validate_name_callback(self, name):
        if (name is not None) and (len(name) > 0):
            return dtoolcore.utils.name_is_valid(name)
        return True

    def _update_name(self, event):
        widget = event.widget
        name = widget.get()
        if (name is not None) and name != "":
            logger.info("Setting dataset name to: {}".format(name))
            self.master.proto_dataset_model.set_name(name)
        self.refresh()
        self.data_directory_btn.focus_set()

    def _setup_name_input_field(self, row):

        vcmd = (self.master.register(self._validate_name_callback), "%P")
        lbl = ttk.Label(self.label_frame, text="Dataset Name")
        entry = ttk.Entry(
            self.label_frame,
            validate="key",
            validatecommand=vcmd,
        )

        current_name = self.master.proto_dataset_model.name
        if current_name is not None:
            entry.insert(0, current_name)

        entry.bind("<FocusOut>", self._update_name)
        entry.bind("<Return>", self._update_name)
        entry.bind("<Tab>", self._update_name)

        lbl.grid(row=row, column=0, sticky="e")
        entry.grid(row=row, column=1, sticky="ew")

    def _select_data_directory_event(self, event):
        self._select_data_directory()

    def _select_data_directory(self):
        data_directory = fd.askdirectory(
            title="Select data directory",
            initialdir=HOME_DIR
        )
        self.master.proto_dataset_model.set_input_directory(data_directory)
        logger.info("Data directory set to: {}".format(data_directory))
        self.refresh()
        self.metadata_schema_combobox.focus_set()

    def _setup_input_directory_field(self, row):
        lbl = ttk.Label(self.label_frame, text="Input data directory")
        logger.info("Current input directory: {}".format(
            self.master.proto_dataset_model.input_directory
        ))
        entry = ttk.Entry(
            self.label_frame,
            )
        current_input_dir = self.master.proto_dataset_model.input_directory
        if current_input_dir is not None:
            entry.insert(0, current_input_dir)
        entry.configure(state="readonly")

        self.data_directory_btn = ttk.Button(
            self.label_frame,
            text="Select data directory",
            command=self._select_data_directory
        )
        lbl.grid(row=row, column=0, sticky="e")
        entry.grid(row=row, column=1, sticky="ew")
        self.data_directory_btn.grid(row=row, column=2, sticky="w")
        self.data_directory_btn.bind("<Return>", self._select_data_directory_event)  # NOQA

    def _setup_metadata_schema_selection(self, row):
        lbl = ttk.Label(self.label_frame, text="Select metadata schema")

        # Get the schema names and make sure that there is a schema named
        # "basic".
        schema_selection = self.master.metadata_schema_list_model.metadata_model_names  # NOQA
        assert "basic" in schema_selection

        self.metadata_schema_combobox = ttk.Combobox(
            self.label_frame,
            state="readonly",
            values=schema_selection
        )
        self.metadata_schema_combobox.bind("<<ComboboxSelected>>", self._select_metadata_schema)  # NOQA

        # Set the default.
        index = schema_selection.index("basic")
        self.metadata_schema_combobox.current(index)

        lbl.grid(row=row, column=0)
        self.metadata_schema_combobox.grid(row=row, column=1)

    def _select_metadata_schema(self, event):
        widget = event.widget
        value = widget.get()
        self._update_metadata_schema(value)

    def _update_metadata_schema(self, schema_name):
        metadata_model = self.master.metadata_schema_list_model.get_metadata_model(schema_name)  # NOQA
        self.master.metadata_model = metadata_model
        self.master.proto_dataset_model.set_metadata_model(metadata_model)
        self.master.refresh()

    def refresh(self):
        """Refresh new dataset config frame."""
        logger.info("Refreshing {}".format(self))
        for widget in self.label_frame.winfo_children():
            widget.destroy()

        self._setup_name_input_field(0)
        self._setup_input_directory_field(1)
        self._setup_metadata_schema_selection(3)


class OptionalMetadataFrame(ttk.Frame):
    """Optional metadata frame."""

    def __init__(self, master, root):
        super().__init__(master)
        logger.info("Initialising {}".format(self))
        self.master = master
        self.root = root
        self.label_frame = ttk.LabelFrame(self, text="Optional metadata")  # NOQA
        self.label_frame.grid(row=0, column=0)

        self.optional_metadata_listbox = tk.Listbox(self.label_frame)
        self.optional_metadata_listbox.bind(
            "<<ListboxSelect>>",
            self.master.select_optional_metadata
        )
        self.optional_metadata_listbox.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.refresh()

    @property
    def metadata_model(self):
        return self.master.proto_dataset_model.metadata_model

    def refresh(self):
        """Refresh optional metadata frame."""
        self.optional_metadata_listbox.delete(0, tk.END)
        for name in self.metadata_model.deselected_optional_item_names:
            logger.info("Adding {} to optional metadata listbox".format(name))
            self.optional_metadata_listbox.insert(tk.END, name)


class MetadataFormFrame(ttk.Frame):
    """Metadata form frame."""

    def __init__(self, master, root):
        super().__init__(master)
        logger.info("Initialising {}".format(self))
        self.master = master
        self.root = root
        self.entries = {}
        self.label_frame = ttk.LabelFrame(self, text="Metadata form")  # NOQA
        self.label_frame.grid(row=0, column=0, sticky="nsew")
        self.refresh()

    @property
    def metadata_model(self):
        return self.master.proto_dataset_model.metadata_model

    def _value_update_event(self, event):
        widget = event.widget
        name = widget.name
        value_as_str = widget.get()
        if (value_as_str is not None) and (value_as_str != ""):
            logger.info(f"Setting {name} to: {value_as_str}")
            self.metadata_model.set_value_from_str(name, value_as_str)
        self.refresh()

    def value_update_event_focus_out(self, event):
        self._value_update_event(event)

    def value_update_event_focus_next(self, event):
        widget = event.widget
        name = widget.name
        self._value_update_event(event)
        index = self.metadata_model.in_scope_item_names.index(name)  # NOQA
        next_index = index + 1
        if next_index >= len(self.metadata_model.in_scope_item_names):  # NOQA
            next_index = 0
        next_name = self.metadata_model.in_scope_item_names[next_index]  # NOQA
        self.entries[next_name].focus_set()

    def setup_boolean_input_field(self, row, name, value):
        values = ["True", "False"]
        e = ttk.Combobox(self.label_frame, state="readonly", values=values)
        _set_combobox_default_selection(e, values, value)
        e.name = name
        e.bind("<<ComboboxSelected>>", self.value_update_event_focus_next)
        e.bind("<Return>", self.value_update_event_focus_next)
        e.grid(row=row, column=1, sticky="ew")
        self.entries[name] = e

    def setup_entry_input_field(self, row, name, value):
        e = tk.Entry(self.label_frame)
        if value is not None:
            e.insert(0, str(value))
        e.name = name
        e.bind("<FocusOut>", self.value_update_event_focus_out)
        e.bind("<Return>", self.value_update_event_focus_next)
        e.bind("<Tab>", self.value_update_event_focus_next)
        e.grid(row=row, column=1, sticky="ew")
        self.entries[name] = e

    def setup_enum_input_field(self, row, name, value):
        schema = self.master.metadata_model.get_schema(name)
        values = [str(v) for v in schema.enum]
        e = ttk.Combobox(self.label_frame, state="readonly", values=values)
        _set_combobox_default_selection(e, values, value)
        e.name = name
        e.bind("<<ComboboxSelected>>", self.value_update_event_focus_next)
        e.grid(row=row, column=1, sticky="ew")
        self.entries[name] = e

    def setup_input_field(self, row, name):
        """Setup metadata form input field."""
        schema = self.metadata_model.get_schema(name)

        # Create the label.
        display_name = name
        if name in self.metadata_model.required_item_names:
            display_name = name + "*"

        lbl = tk.Label(self.label_frame, text=display_name)
        lbl.grid(row=row, column=0, sticky="e")

        value = self.metadata_model.get_value(name)

        # Create the input field.
        if schema.type == "boolean":
            self.setup_boolean_input_field(row, name, value)
        elif schema.enum is None:
            self.setup_entry_input_field(row, name, value)
        else:
            self.setup_enum_input_field(row, name, value)

        # Add button to enable the removal of the field if it is optional.
        if name in self.metadata_model.optional_item_names:
            btn = tk.Button(self.label_frame, text="Remove")
            btn._name_to_clear = name
            btn.bind("<Button-1>", self.master.deselect_optional_metadata)
            btn.grid(row=row, column=2)

        # Highlight input field if the value is invalid.
        background = "white"
        if value is not None and not self.metadata_model.is_okay(name):
            background = "pink"
            for issue in self.metadata_model.issues(name):
                row = row + 1
                issue_lbl = ttk.Label(self.label_frame, text=issue)
                issue_lbl.grid(row=row, column=1, columnspan=2, sticky="w")
        self.entries[name].config({"background": background})

        return row + 1

    def refresh(self):
        """Refresh metadata form frame."""
        logger.info("Refreshing {}".format(self))
        for widget in self.label_frame.winfo_children():
            widget.destroy()

        row = 0
        for name in self.metadata_model.in_scope_item_names:  # NOQA
            logger.info("Adding {} to metadata form frame".format(name))
            row = self.setup_input_field(row, name)


class NewDataSetWindow(tk.Toplevel):
    """Preferences window."""

    def __init__(self, master):
        super().__init__(master)
        logger.info("Initialising {}".format(self))
        self.title("New dataset")
        self.focus_set()
        self.root = master

        self.metadata_schema_list_model = MetadataSchemaListModel()
        self.metadata_schema_list_model.put_metadata_schema_directory(METADATA_SCHEMAS_DIR)  # NOQA
        assert "basic" in self.metadata_schema_list_model.metadata_model_names
        default_metadata_model = self.metadata_schema_list_model.get_metadata_model("basic")  # NOQA

        self.proto_dataset_model = ProtoDataSetModel()
        self.proto_dataset_model.set_base_uri_model(self.master.base_uri_model)
        self.proto_dataset_model.set_metadata_model(default_metadata_model)

        # If we use the code below for styling the NewDataSetConfigFrame,
        # OptionalMetadataFrame, MetadataFormFrame and ttk.Button need to have
        # mainframe as their first argument. However, some of these currently
        # call select_optional_metadata, deselect_optional_metadata, create
        # and refresh. That stops working in that case as they are not on the
        # mainframe object. The only reason to change to the below is to do
        # with background styling of the tk.Toplevel window.
#       mainframe = ttk.Frame(self)
#       mainframe.grid(row=0, column=0, sticky="nwes")

        self.new_dataset_config_frame = NewDataSetConfigFrame(self, self.root)
        self.new_dataset_config_frame.grid(row=0, column=0, columnspan=2)

        self.optional_metadata_frame = OptionalMetadataFrame(self, self.root)
        self.optional_metadata_frame.grid(row=1, column=0, sticky="nsew")

        self.metadata_form_frame = MetadataFormFrame(self, self.root)
        self.metadata_form_frame.grid(row=1, column=1, sticky="nsew")

        self.create_btn = ttk.Button(self, text="Create", command=self.create)
        self.create_btn.grid(row=2, column=0, columnspan=2, sticky="we")

    def select_optional_metadata(self, event):
        widget = event.widget
        try:
            index = int(widget.curselection()[0])
        except IndexError:
            return
        name = widget.get(index)
        logger.info(f"Selected optional metadata: {name}")
        self.proto_dataset_model.metadata_model.select_optional_item(name)
        self.refresh()
        self.metadata_form_frame.entries[name].focus_set()

    def deselect_optional_metadata(self, event):
        widget = event.widget
        name = widget._name_to_clear
        logger.info(f"Deselected optional metadata: {name}")
        self.proto_dataset_model.metadata_model.deselect_optional_item(name)
        self.refresh()

    def _check_create_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self._check_create_thread(thread))
        else:
            self.create_btn.config(state=tk.NORMAL)
            self.progressbar.destroy()
            self.master.refresh()

    def _run_create(self):
        try:
            self.proto_dataset_model.create(progressbar=self.progressbar)
        except Exception as e:
            logger.warning("Dataset creation exception: {}".format(e))
            mb.showwarning("Failed to create dataset", e)
        logger.info("Finished dataset creation")

    def create(self):
        # Need to check this as _yield_path_handle_tuples will fail if the
        # input directory has not been set.
        if self.proto_dataset_model.input_directory is None:
            mb.showwarning(
                "Failed to create dataset",
                "Input directory has not been set"
            )
            return

        if self.root.base_uri_model.get_base_uri() is None:
            mb.showwarning(
                "Failed to create dataset",
                "Local base URI has not been configured. Configure it in the preferences."  # NOQA
            )
            return

        # The number of items is needed for the progress bar.
        num_items = len(list(self.proto_dataset_model._yield_path_handle_tuples()))  # NOQA
        self.progressbar = NewDataSetProgressBar(self, maximum=num_items)
        self.progressbar.grid(row=3, column=0, columnspan=2, sticky="we")

        # Disable the "create" button whilst the creation process is happening.
        self.create_btn.config(state=tk.DISABLED)

        # Create and start the dataset creation in a separate thread.
        thread = threading.Thread(target=self._run_create)
        logger.info("Start creation thread")
        thread.start()

        # Call function that will continue polling until the thread is done.
        self._check_create_thread(thread)

    def refresh(self):
        self.optional_metadata_frame.refresh()
        self.metadata_form_frame.refresh()


class PreferencesWindow(tk.Toplevel):
    """Preferences window."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Preferences")

        logger.info("Initialising {}".format(self))
        self.root = master
        mainframe = ttk.Frame(self)
        mainframe.grid(row=0, column=0, sticky="nwes")
        label_frame = ttk.LabelFrame(mainframe, text="Local base URI directory")  # NOQA
        label_frame.grid(row=0, column=0,)
        self.local_base_uri_directory = tk.StringVar()
        self.local_base_uri_directory.set(
            self.root.base_uri_model.get_base_uri()
        )
        label = ttk.Label(label_frame, textvar=self.local_base_uri_directory)
        button = ttk.Button(
            label_frame,
            text="Select local base URI directory",
            command=self.select_local_base_uri_directory
        )
        label.grid(row=0, column=0)
        button.grid(row=1, column=0)

    def select_local_base_uri_directory(self):
        base_uri_directory = fd.askdirectory(
            title="Select data directory",
            initialdir=HOME_DIR
        )
        self.root.base_uri_model.put_base_uri(base_uri_directory)
        self.local_base_uri_directory.set(base_uri_directory)
        logger.info(
            "Local base URI directory set to: {}".format(
                base_uri_directory
            )
        )
        self.root.refresh()


class NewDataSetProgressBar(ttk.Progressbar):

    def __init__(self, master, maximum):
        super().__init__(master, maximum=maximum)
        logger.info("Initialising {}".format(self))
        self.current = 0
        self._maximum = maximum

    @property
    def total(self):
        return self._maximum

    def update(self, steps):
        self.current = self.current + steps
        self.config(value=self.current)


class App(tk.Tk):
    """Root tkinter application."""

    def __init__(self):
        super().__init__()
        logger.info("Initialising dtool-gui")
        self.title("dtool")

        # Make sure that the GUI expands/shrinks when the window is resized.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Initialise the models.
        self.base_uri_model = LocalBaseURIModel()
        self.dataset_list_model = DataSetListModel()
        self.dataset_model = DataSetModel()

        # Configure the models.
        self.dataset_list_model.set_base_uri_model(self.base_uri_model)
        if len(self.dataset_list_model.names) > 0:
            first_uri = self.dataset_list_model.get_uri(0)
            self.load_dataset(first_uri)

        # Determine the platform.
        self.platform = self.tk.call("tk", "windowingsystem")
        logger.info("Running on platform: {}".format(self.platform))

        # Remove ability to tear off menu on Windows and X11.
        self.option_add("*tearOff", False)

        # Create the menubar.
        menubar = tk.Menu(self)

        # Make Mac menubar display name of app instead of python.
        if self.platform == "aqua":
            appmenu = tk.Menu(menubar, name="apple")
            menubar.add_cascade(menu=appmenu)
            appmenu.add_command(label="About dtool")
            appmenu.add_separator()

        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label="File")
        menu_edit = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_edit, label="Edit")

        # Add content to the menus.
        self._add_menu_command(
            menu=menu_file,
            label="New dataset...",
            accelerator_key="N",
            cmd=self.new_dataset,
            event_cmd=self._new_dataset_event
        )

        if self.platform != "aqua":
            menu_file.add_separator()
            self._add_menu_command(
                menu=menu_file,
                label="Quit",
                accelerator_key="Q",
                cmd=self.quit,
                event_cmd=self._quit_event
            )

        self._add_menu_command(
            menu=menu_edit,
            label="Edit metadata...",
            accelerator_key="M",
            cmd=self.edit_metadata,
            event_cmd=self._edit_metadata_event
        )

        if self.platform != "aqua":
            self._add_menu_command(
                menu=menu_edit,
                label="Edit preferences...",
                accelerator_key="P",
                cmd=self.show_perferences_window,
                event_cmd=self._show_perferences_window_event
            )

        # Deal with preferences menu item on Mac.
        self.createcommand("tk::mac::ShowPreferences", self.show_perferences_window)  # NOQAQ

        self.config(menu=menubar)

        self.mainframe = ttk.Frame(self)
        self.mainframe.grid(row=0, column=0, sticky="nwes")

        # Make sure that the GUI expands/shrinks when the window is resized.
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.dataset_list_frame = DataSetListFrame(self.mainframe, self)
        self.dataset_list_frame.grid(row=0, column=0, sticky="nsew")

        self.dataset_frame = DataSetFrame(self.mainframe, self)
        self.dataset_frame.grid(row=0, column=1, sticky="new")

        # Ask the user to configure the local base URI if it has not been configured.  # NOQA
        if self.base_uri_model.get_base_uri() is None:
            mb.showinfo(
                "Configure local base URI",
                "Please configure the local base URI in the preferences."
                "This is where datasets will be created on your computer."
            )

    def _get_accelerator(self, key):
        key = key.upper()
        if self.platform == "aqua":
            return "Cmd+{}".format(key)
        return "Ctrl+{}".format(key)

    def _get_accelerator_binding(self, key):
        key = key.lower()
        if self.platform == "aqua":
            return "<Command-{}>".format(key)
        return "<Control-{}>".format(key)

    def _add_menu_command(self, menu, label, accelerator_key, cmd, event_cmd):
        menu.add_command(
            label=label,
            accelerator=self._get_accelerator(accelerator_key),
            command=cmd
        )
        self.bind_all(
            self._get_accelerator_binding(accelerator_key),
            event_cmd
        )

    def _new_dataset_event(self, event):
        self.new_dataset()

    def new_dataset(self):
        """Open window with form to create a new dataset."""
        logger.info(self.new_dataset.__doc__)
        NewDataSetWindow(self)

    def _edit_metadata_event(self, event):
        self.edit_metadata()

    def edit_metadata(self):
        """Open window with form to edit a dataset's metadata."""
        logger.info(self.edit_metadata.__doc__)
        mb.showinfo(
            "Work in progress...",
            "It is not possible to edit an existing dataset's metadata yet."
        )

    def _quit_event(self, event):
        self.quit()

    def quit(self):
        """Quit the dtool-gui application."""
        logger.info(self.quit.__doc__)

    def _show_perferences_window_event(self, event):
        self.show_perferences_window()

    def show_perferences_window(self):
        """Show the preferences window."""
        logger.info(self.show_perferences_window.__doc__)
        PreferencesWindow(self)

    def load_dataset(self, dataset_uri):
        """Load dataset and deal with UnsupportedTypeError exceptions."""
        try:
            self.dataset_model.load_dataset(dataset_uri)
        except UnsupportedTypeError:
            logging.warning("Dataset contains unsupported metadata type")

    def refresh(self):
        """Refreshing all frames."""
        logger.info(self.refresh.__doc__)
        self.dataset_list_frame.refresh()
        self.dataset_frame.refresh()


def tkgui(debug_level=logging.WARNING):
    """Start the tkinter app."""
    logging.basicConfig(level=debug_level)
    app = App()
    app.mainloop()


if __name__ == "__main__":
    num_args = len(sys.argv) - 1
    if num_args == 0:
        tkgui()
    if num_args == 1:
        debug_level = sys.argv[1].upper()
        acceptable_debug_levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEGUG", "NOTSET")  # NOQA
        if debug_level not in acceptable_debug_levels:
            print("Error: {} not in {}".format(debug_level, acceptable_debug_levels))  # NOQA
            sys.exit(2)
        tkgui(debug_level)
    else:
        print("Error: Too many arguments")
        sys.exit(2)
