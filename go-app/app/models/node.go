package models

import "github.com/Danila331/HACH-T1/app/store"

type Node struct {
	ID         int
	Type       string
	Text       string
	ShouldToDo string
}

type NodeInterface interface {
	Create() error
	Update() error
	Delete() error
	ReadAll() ([]Node, error)
	ReadByID() (Node, error)
}

func (n *Node) Create() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("INSERT INTO nodes (type, text, should_to_do) VALUES ($1, $2, $3)", n.Type, n.Text, n.ShouldToDo)
	if err != nil {
		return err
	}
	return nil
}

func (n *Node) Update() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("UPDATE nodes SET type = $1, text = $2, should_to_do = $3 WHERE id = $4", n.Type, n.Text, n.ShouldToDo, n.ID)
	if err != nil {
		return err
	}
	return nil
}

func (n *Node) Delete() error {
	conn, err := store.ConnectDB()
	if err != nil {
		return err
	}
	defer conn.Close()
	_, err = conn.Exec("DELETE FROM nodes WHERE id = $1", n.ID)
	if err != nil {
		return err
	}
	return nil
}

func (n *Node) ReadAll() ([]Node, error) {
	conn, err := store.ConnectDB()
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	rows, err := conn.Query("SELECT * FROM nodes")
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var nodes []Node
	for rows.Next() {
		var node Node
		err = rows.Scan(&node.ID, &node.Type, &node.Text, &node.ShouldToDo)
		if err != nil {
			return nil, err
		}
		nodes = append(nodes, node)
	}
	return nodes, nil
}

func (n *Node) ReadByID() (Node, error) {
	conn, err := store.ConnectDB()
	if err != nil {
		return Node{}, err
	}
	defer conn.Close()
	row := conn.QueryRow("SELECT * FROM nodes WHERE id = $1", n.ID)
	var node Node
	err = row.Scan(&node.ID, &node.Type, &node.Text, &node.ShouldToDo)
	if err != nil {
		return Node{}, err
	}
	return node, nil
}
